#!/usr/bin/env python3
"""
lsb-flag-finder — Extract LSB data from images and grep for CTF flags
across multiple encodings (ASCII, Base64, Base32, ROT13).

Usage:
    python lsb_flag_finder.py image.png
    python lsb_flag_finder.py image.png --bits 2 --channels RG
    python lsb_flag_finder.py image.png --encoding base64
    python lsb_flag_finder.py image.png --flag-format "myctf{.*}"
    python lsb_flag_finder.py image.png --raw > output.bin
"""

import argparse
import base64
import codecs
import re
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow required — pip install Pillow", file=sys.stderr)
    sys.exit(1)

# ── Flag patterns ───────────────────────────────────────────────────────────
FLAG_PATTERNS = [
    r"flag\{[^}]+\}",
    r"ctf\{[^}]+\}",
    r"picoCTF\{[^}]+\}",
    r"HTB\{[^}]+\}",
    r"THM\{[^}]+\}",
    r"DEAD\{[^}]+\}",
    r"KEY\{[^}]+\}",
    r"SEC\{[^}]+\}",
    r"[A-Za-z0-9_]{2,20}\{[^}]{3,}\}",  # generic PREFIX{...}
]
DEFAULT_RE = re.compile("|".join(FLAG_PATTERNS), re.IGNORECASE)

CHANNEL_MAP = {"R": 0, "G": 1, "B": 2, "A": 3}


# ── LSB extraction ─────────────────────────────────────────────────────────
def extract_lsb(path: str, bits: int = 1, channels: str = "RGB") -> bytes:
    """Pull the lowest `bits` from each pixel channel and pack into bytes."""
    img = Image.open(path).convert("RGBA")
    px = img.load()
    w, h = img.size
    targets = [CHANNEL_MAP[c] for c in channels.upper() if c in CHANNEL_MAP]
    mask = (1 << bits) - 1

    raw_bits: list[int] = []
    for y in range(h):
        for x in range(w):
            pixel = px[x, y]
            for ch in targets:
                raw_bits.append(pixel[ch] & mask)

    # pack into bytes
    out = bytearray()
    buf = 0
    count = 0
    for val in raw_bits:
        for i in range(bits - 1, -1, -1):
            buf = (buf << 1) | ((val >> i) & 1)
            count += 1
            if count == 8:
                out.append(buf)
                buf = 0
                count = 0
    return bytes(out)


# ── Decoders ────────────────────────────────────────────────────────────────
def _printable(data: bytes) -> str:
    """Return printable ASCII subset."""
    return "".join(c for c in data.decode("ascii", errors="ignore") if 32 <= ord(c) <= 126 or c in "\n\r\t")


def decode_ascii(data: bytes) -> str | None:
    text = _printable(data)
    return text if text.strip() else None


def decode_base64(data: bytes) -> str | None:
    text = _printable(data)
    hits: list[str] = []
    for m in re.finditer(r"[A-Za-z0-9+/]{16,}={0,3}", text):
        try:
            decoded = base64.b64decode(m.group(), validate=True).decode("utf-8", errors="ignore")
            if decoded.strip():
                hits.append(decoded)
        except Exception:
            continue
    return "\n".join(hits) if hits else None


def decode_base32(data: bytes) -> str | None:
    text = _printable(data)
    hits: list[str] = []
    for m in re.finditer(r"[A-Z2-7]{16,}={0,6}", text):
        try:
            decoded = base64.b32decode(m.group()).decode("utf-8", errors="ignore")
            if decoded.strip():
                hits.append(decoded)
        except Exception:
            continue
    return "\n".join(hits) if hits else None


def decode_rot13(data: bytes) -> str | None:
    text = _printable(data)
    if not text.strip():
        return None
    return codecs.decode(text, "rot_13")


DECODERS = {
    "ascii": decode_ascii,
    "base64": decode_base64,
    "base32": decode_base32,
    "rot13": decode_rot13,
}


# ── Flag grep ──────────────────────────────────────────────────────────────
def grep_flags(text: str, pattern: re.Pattern = DEFAULT_RE) -> list[str]:
    return list(set(pattern.findall(text))) if text else []


# ── CLI ─────────────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(
        prog="lsb-flag-finder",
        description="Extract LSB from images → decode → grep CTF flags",
    )
    ap.add_argument("image", help="Image file path (PNG, BMP, TIFF, etc.)")
    ap.add_argument("--bits", type=int, default=1, choices=[1, 2, 3, 4], help="LSBs to extract per channel (default: 1)")
    ap.add_argument("--channels", default="RGB", help="Channels to read (default: RGB)")
    ap.add_argument("--encoding", choices=["ascii", "base64", "base32", "rot13", "all"], default="all", help="Decoding to try (default: all)")
    ap.add_argument("--flag-format", help="Custom flag regex, e.g. 'myctf{.*}'")
    ap.add_argument("--raw", action="store_true", help="Dump raw LSB bytes to stdout")
    ap.add_argument("-v", "--verbose", action="store_true", help="Show previews even without flag hits")

    args = ap.parse_args()

    if not Path(args.image).is_file():
        ap.error(f"File not found: {args.image}")

    # Extract
    print(f"[*] Extracting {args.bits}-bit LSB from {args.channels} channels …")
    raw = extract_lsb(args.image, args.bits, args.channels)
    print(f"[*] Got {len(raw):,} bytes")

    if args.raw:
        sys.stdout.buffer.write(raw)
        return

    # Prepare flag regex
    pat = re.compile("|".join(FLAG_PATTERNS + [args.flag_format]), re.IGNORECASE) if args.flag_format else DEFAULT_RE

    # Decode + grep
    encodings = list(DECODERS) if args.encoding == "all" else [args.encoding]
    found = False

    for enc in encodings:
        decoded = DECODERS[enc](raw)
        if decoded is None:
            continue
        flags = grep_flags(decoded, pat)
        if flags:
            found = True
            print(f"\n[+] FLAGS FOUND  [{enc.upper()}]")
            for f in flags:
                print(f"    >>> {f}")
        elif args.verbose:
            preview = decoded[:300].strip()
            if preview:
                print(f"\n[~] {enc.upper()} — no flags, preview:")
                print(f"    {preview[:200]}")

    if not found:
        print("\n[-] No flags found. Try --verbose, --bits 2, or different --channels.")


if __name__ == "__main__":
    main()
