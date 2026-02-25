<div align="center">

# 🚩 CTF-TOOLS — Image Forensics Toolkit

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-GPL%20v3-blue?style=for-the-badge)
![CTF](https://img.shields.io/badge/CTF-Forensics-red?style=for-the-badge&logo=hackthebox&logoColor=white)
![Category](https://img.shields.io/badge/Category-Steganography%20%7C%20Forensics-purple?style=for-the-badge)

**A collection of Python-based image forensics and repair tools for Capture The Flag (CTF) competitions.**

Repair corrupted image files, validate headers, fix CRC checksums, and recover hidden data from PNG, JPEG, GIF, and BMP files — essential tools for solving steganography and forensics challenges.

</div>

---

## 📋 Table of Contents

- [Tools Included](#-tools-included)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Supported Formats](#-supported-formats)
- [Contributing](#-contributing)

---

## 🧰 Tools Included

| Tool | Purpose | Supported Formats |
|------|---------|-------------------|
| **Image-Fixer.py** | Universal image repair — validates magic bytes, parses chunks, fixes headers | PNG, JPEG, GIF, BMP |
| **OriginalPNG-fixer.py** | Interactive PNG repair — CRC validation, chunk type repair, manual header correction | PNG |
| **png-fixer.py** | Automated PNG repair — header alignment, IHDR detection, chunk integrity validation | PNG |

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| **Magic Byte Validation** | Detects and repairs corrupted file headers (PNG signature, JPEG SOI, GIF87a/89a, BMP) |
| **Chunk Parsing** | Parses image file chunks (IHDR, IDAT, IEND, PLTE, tEXt, etc.) with proper length validation |
| **CRC Verification** | Validates CRC32 checksums for each chunk and auto-repairs mismatches |
| **Header Injection** | Inserts missing JFIF/Exif headers in JPEG files |
| **IHDR Alignment** | Detects misaligned IHDR chunks in PNG files and realigns to correct offset |
| **Interactive Repair** | OriginalPNG-fixer offers manual chunk type selection for complex corruptions |
| **Auto-Truncation** | Removes trailing garbage data after IEND chunk |
| **Multi-Format** | Single tool (Image-Fixer.py) handles PNG, JPEG, GIF, and BMP formats |

---

## 🛠️ Tech Stack

| Component | Technology | Role |
|-----------|-----------|------|
| **Language** | Python 3.x | Core programming language |
| **Binary Parsing** | `struct` | Unpacking binary data (big-endian chunk lengths, CRC values) |
| **Checksum** | `binascii.crc32` | CRC32 computation for PNG chunk validation |
| **I/O** | `sys` + file I/O | Command-line args and binary file read/write |
| **Architecture** | OOP (`FileRepairer` class) | Modular, extensible repair framework |

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/cazy8/CTF-TOOLS.git
cd CTF-TOOLS

# No external dependencies required — uses Python standard library only
python3 --version  # Requires Python 3.6+
```

> **Zero dependencies** — all tools use only the Python standard library (`struct`, `binascii`, `sys`).

---

## ⚙️ Usage

### Image-Fixer.py (Universal — PNG/JPEG/GIF/BMP)

```bash
python3 Image-Manipulation/Image-Fixer.py <input_image> <output_image>
```

```bash
# Fix a corrupted PNG
python3 Image-Manipulation/Image-Fixer.py corrupted.png fixed.png

# Fix a broken JPEG
python3 Image-Manipulation/Image-Fixer.py broken.jpg repaired.jpg

# Repair a GIF file
python3 Image-Manipulation/Image-Fixer.py challenge.gif solved.gif
```

### OriginalPNG-fixer.py (Interactive PNG Repair)

```bash
python3 Image-Manipulation/OriginalPNG-fixer.py <input.png> <output.png>
```

- Walks through each chunk interactively
- Prompts for manual chunk type selection when type is invalid
- Shows expected vs actual CRC values
- Auto-repairs CRC mismatches and length errors

### png-fixer.py (Automated PNG Repair)

```bash
python3 Image-Manipulation/png-fixer.py <input.png> <output.png>
```

- Fully automated — no user interaction needed
- Best for quick fixes during timed CTF competitions

---

## 🔬 How It Works

### PNG File Structure

```
┌──────────────────┐
│  PNG Signature    │  8 bytes: 89 50 4E 47 0D 0A 1A 0A
├──────────────────┤
│  IHDR Chunk       │  Image header (width, height, bit depth, color type)
├──────────────────┤
│  PLTE Chunk       │  Palette (optional, for indexed color images)
├──────────────────┤
│  IDAT Chunk(s)    │  Compressed image data (can be multiple)
├──────────────────┤
│  tEXt/iTXt        │  Metadata chunks (may contain hidden flags!)
├──────────────────┤
│  IEND Chunk       │  End marker
└──────────────────┘

Each chunk:
┌────────┬────────┬──────────────┬─────────┐
│ Length  │  Type  │     Data     │   CRC   │
│ 4 bytes│ 4 bytes│ Length bytes  │ 4 bytes │
└────────┴────────┴──────────────┴─────────┘
```

### Repair Pipeline

```
Input File → Validate Magic Bytes → Fix Header if Invalid
                                          │
                                          ▼
                                   Parse Chunks
                                          │
                              ┌───────────┼───────────┐
                              ▼           ▼           ▼
                         Validate    Validate     Validate
                          Type       Length         CRC
                              │           │           │
                              ▼           ▼           ▼
                         Repair if   Repair if   Repair if
                          Invalid     Invalid     Invalid
                              │           │           │
                              └───────────┼───────────┘
                                          ▼
                                   Write Output
```

---

## 📝 Supported Formats

| Format | Magic Bytes | Tools |
|--------|-------------|-------|
| **PNG** | `89 50 4E 47 0D 0A 1A 0A` | All three tools |
| **JPEG/JPG** | `FF D8 FF` | Image-Fixer.py |
| **GIF** | `47 49 46 38 37 61` (GIF87a) | Image-Fixer.py |
| **BMP** | `42 4D` (BM) | Image-Fixer.py |

### Validated PNG Chunk Types

```
IHDR  PLTE  IDAT  IEND  bKGD  cHRM  dSIG  eXIf
gAMA  hIST  iCCP  iTXt  pHYs  sBIT  sPLT  sRGB
sTER  tEXt  tIME  tRNS  zTXt
```

---

## 💡 CTF Tips

| Scenario | Tool to Use | What to Look For |
|----------|------------|-----------------|
| Image won't open | Image-Fixer.py | Corrupted magic bytes / header |
| PNG shows wrong dimensions | OriginalPNG-fixer.py | Modified IHDR width/height values |
| CRC error in PNG viewer | png-fixer.py | Intentionally broken CRC (common CTF trick) |
| Hidden data in metadata | OriginalPNG-fixer.py | Suspicious tEXt/iTXt chunks |
| JPEG missing JFIF header | Image-Fixer.py | SOI present but APP0 missing |
| Flag hidden after IEND | Manual hex analysis | Data appended after PNG end marker |

---

## 📁 Project Structure

```
CTF-TOOLS/
├── Image-Manipulation/
│   ├── Image-Fixer.py           # Universal format repair (OOP-based)
│   ├── OriginalPNG-fixer.py     # Interactive PNG-specific repair
│   └── png-fixer.py             # Automated PNG repair
├── LICENSE                       # GPL v3
└── README.md                     # Documentation
```

---

## 🤝 Contributing

Contributions welcome! Ideas for expansion:

- 🔊 **Audio Forensics** — WAV/MP3 header repair and spectrogram analysis
- 📦 **ZIP/RAR Repair** — Archive header fixing for misc challenges
- 🔐 **Steganography Detection** — LSB extraction, zsteg/stegsolve integration
- 📋 **PCAP Analysis** — Network forensics toolkit
- 🧮 **Crypto Helpers** — Common cipher solvers (Caesar, XOR, Vigenère)

---

## 👤 Author

**Harsh Gupta** — [@cazy8](https://github.com/cazy8) · [LinkedIn](https://www.linkedin.com/in/h4rshg/)

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**If you found this useful, consider giving it a ⭐**

</div>
