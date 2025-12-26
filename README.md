# img2pdf Application

The img2pdf application is a Python-based tool designed to convert image files into `PDF` format. It leverages the `Pillow` library, a powerful and flexible library for opening, manipulating, and saving many different image file formats.

## Features:
Converts single or multiple image files into a PDF document
Supports various image formats (e.g., JPG, PNG, BMP, etc.)
Allows customization of output PDF settings
Provides error handling for robust performance

## Requirements:
- Python 3.x
- Pillow library (`pip3 install Pillow`)

## Installation

1. clone repository
2. check if you have `python3` & `pip3` installed:
```bash
python3 --version
# sample output:
# Python 3.14.2
pip3 --version
# sample output:
# pip 25.3 from /opt/homebrew/lib/python3.14/site-packages/pip (python 3.14)
```   
3. If no python, install:
```bash
brew install python
```
4. Check if you have `Pillow` installed:
```bash
```bash
pip3 list
# sample output
# Package Version
# ------- -------
# pillow  12.0.0
# pip     25.3
# wheel   0.45.1
```
5. If no Pillow, install:
```bash
pip3 install Pillow
```
6. Use next section to get further instructions

# How to Use

## Method 1: Command Line

```bash
# Make the script executable
chmod +x img2pdf_converter.py

# Convert single image
python3 img2pdf_converter.py photo.jpg

# Convert with A4 paper size
python3 img2pdf_converter.py photo.jpg --resize-a4

# Convert multiple images to individual PDFs
python3 img2pdf_converter.py "*.jpg"

# Combine multiple images into one PDF
python3 img2pdf_converter.py "*.jpg" -m combined.pdf

# Convert all images in a folder
python3 img2pdf_converter.py ~/Pictures -d

# Use interactive mode
python3 img2pdf_converter.py
```

## Method 2: Drag & Drop (Simple Script)

1. Save the `simple_img2pdf.py` script
2. Drag image files onto the script in Finder
3. PDFs will be created in the same folder

## Method 3: Create an Automator Service (Mac-specific)

1. Open Automator
2. Choose Quick Action
3. Set:
  - **Workflow receives:** files or folders in Finder
  - **Add "Run Shell Script"** action
4. Enter this script:

```bash
for f in "$@"
do
    /usr/bin/python3 /path/to/your/img2pdf_converter.py "$f"
done
```
5. Save as "Convert to PDF"
6. Now right-click any image in Finder → Services → Convert to PDF

# Features
- **Supports multiple formats:** JPG, PNG, BMP, GIF, TIFF, WebP
- **Single or multi-page PDFs**
- **A4 paper resizing** option
- **Quality control** for compression
- **Batch processing** of entire folders
- **Interactive mode** for easy use
- **Transparency handling** (converts to white background)

The program is lightweight, fast, and produces high-quality PDFs while maintaining the original image resolution by default.
