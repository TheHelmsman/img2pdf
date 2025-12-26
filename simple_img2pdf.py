#!/usr/bin/env python3
"""
Simple drag-and-drop image to PDF converter
"""

import sys
from PIL import Image
import os

def main():
    if len(sys.argv) < 2:
        print("Drag and drop image files onto this script to convert them to PDF.")
        print("Or run from terminal: python3 simple_img2pdf.py image1.jpg [image2.png ...]")
        input("Press Enter to exit...")
        return
    
    for img_path in sys.argv[1:]:
        if os.path.exists(img_path):
            try:
                img = Image.open(img_path)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                pdf_path = os.path.splitext(img_path)[0] + '.pdf'
                img.save(pdf_path, 'PDF', resolution=100.0)
                print(f"Converted: {os.path.basename(img_path)} -> {os.path.basename(pdf_path)}")
                
            except Exception as e:
                print(f"Error converting {img_path}: {e}")
        else:
            print(f"File not found: {img_path}")

if __name__ == "__main__":
    main()