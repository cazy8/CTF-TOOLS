# CTF-TOOLS

CTF Tools is a collection of Python scripts designed to assist participants in Capture The Flag (CTF) competitions and cybersecurity challenges. This project provides various utilities for analyzing network traffic, detecting potential port scanning activities, and more.

## Included Scripts

1. **Image-Fixer.py**: A script to repair and validate image files (PNG, JPEG, GIF, BMP) by checking magic bytes and parsing chunks.
2. **OriginalPNG-fixer.py**: A PNG file fixer that validates and repairs PNG files by checking CRC and chunk types.
3. **png-fixer.py**: Another PNG file fixer that focuses on validating the PNG header and chunk integrity.

## Features

- **Image Repair**: Fixes missing headers and validates image file integrity.
- **Chunk Parsing**: Parses image file chunks and validates their CRC.
- **Error Handling**: Automatically handles errors and attempts to repair corrupted files.

## Requirements

- Python 3.x
- Required Python packages:
  - `scapy` (if applicable)
  - `pandas` (if applicable)
  - `tabulate` (if applicable)
  - `tqdm` (if applicable)
  - `matplotlib` (if applicable)
  - `numpy` (if applicable)

## Installation

-To install the required Python packages, run the following command:

```
pip install scapy pandas tabulate tqdm matplotlib numpy 
```
-If you encounter permission issues, you may need to use sudo:
```sudo pip install scapy pandas tabulate tqdm matplotlib numpy```
## USAGE
Image-Fixer.py
-To run the image fixer script, use the following command structure:

```python3 Image-Fixer.py <input_image> <output_image>```
  -<input_image>: Path to the image file you want to repair.
  -<output_image>: Path where the repaired image will be saved.
  -OriginalPNG-fixer.py
To run the original PNG fixer script, use:
```python3 OriginalPNG-fixer.py <input.png> <output.png>```
  -<input.png>: Path to the PNG file you want to fix.
  -<output.png>: Path where the fixed PNG will be saved.
  -png-fixer.py
To run the PNG fixer script, use:
```python3 png-fixer.py <input.png> <output.png>```
  -<input.png>: Path to the PNG file you want to analyze and fix.
  -<output.png>: Path where the fixed PNG will be saved.
## Notes

Ensure that your image files are valid and accessible.
Processing large image files may take time depending on system resources.
The scripts include error handling to manage invalid files and attempt repairs.

## Contributions are welcome! If you would like to contribute to this project, please fork the repository and submit a pull request.
