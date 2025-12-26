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

## Features
- **Supports multiple formats:** JPG, PNG, BMP, GIF, TIFF, WebP
- **Single or multi-page PDFs**
- **A4 paper resizing** option
- **Quality control** for compression
- **Batch processing** of entire folders
- **Interactive mode** for easy use
- **Transparency handling** (converts to white background)

The program is lightweight, fast, and produces high-quality PDFs while maintaining the original image resolution by default.
