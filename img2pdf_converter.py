#!/usr/bin/env python3
"""
Image to PDF Converter for Mac
Converts one or multiple images to PDF files
"""

import os
import sys
from PIL import Image
from pathlib import Path
import argparse
import glob

def convert_image_to_pdf(image_path, pdf_path=None, resize_to_a4=False, quality=95):
    """
    Convert a single image to PDF
    
    Args:
        image_path: Path to the input image
        pdf_path: Output PDF path (optional, will auto-generate if None)
        resize_to_a4: Whether to resize image to A4 dimensions
        quality: JPEG quality (1-100) for compression
    
    Returns:
        Path to the created PDF file
    """
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Convert RGBA to RGB if necessary (PDF doesn't support transparency)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Create a white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to A4 dimensions if requested (2480x3508 pixels at 300 DPI)
        if resize_to_a4:
            a4_size = (2480, 3508)  # 8.27x11.69 inches at 300 DPI
            image.thumbnail(a4_size, Image.Resampling.LANCZOS)
        
        # Generate output PDF filename if not provided
        if pdf_path is None:
            pdf_path = Path(image_path).with_suffix('.pdf')
        
        # Save as PDF
        image.save(pdf_path, 'PDF', resolution=100.0, quality=quality)
        
        print(f"✓ Converted: {Path(image_path).name} -> {Path(pdf_path).name}")
        return pdf_path
        
    except Exception as e:
        print(f"✗ Error converting {image_path}: {e}")
        return None

def convert_multiple_images_to_pdf(image_paths, output_pdf, resize_to_a4=False, quality=95):
    """
    Convert multiple images to a single multi-page PDF
    
    Args:
        image_paths: List of image paths
        output_pdf: Output PDF file path
        resize_to_a4: Whether to resize images to A4 dimensions
        quality: JPEG quality (1-100) for compression
    """
    images = []
    
    try:
        for img_path in image_paths:
            img = Image.open(img_path)
            
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to A4 if requested
            if resize_to_a4:
                a4_size = (2480, 3508)
                img.thumbnail(a4_size, Image.Resampling.LANCZOS)
            
            images.append(img)
        
        # Save all images as a single PDF
        if images:
            images[0].save(
                output_pdf, 'PDF', 
                resolution=100.0, 
                quality=quality,
                save_all=True, 
                append_images=images[1:]
            )
            print(f"✓ Created multi-page PDF: {output_pdf} ({len(images)} pages)")
            return True
    
    except Exception as e:
        print(f"✗ Error creating multi-page PDF: {e}")
    
    return False

def get_supported_formats():
    """Return a list of supported image formats"""
    return ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']

def main():
    parser = argparse.ArgumentParser(
        description='Convert images to PDF on Mac',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s image.jpg                   # Convert single image
  %(prog)s image.jpg -o output.pdf     # Specify output name
  %(prog)s *.jpg -m combined.pdf       # Combine multiple images into one PDF
  %(prog)s folder/*.png -a4            # Convert with A4 sizing
  %(prog)s -d ~/Pictures               # Convert all images in directory
  
Supported formats: """ + ', '.join(get_supported_formats())
    )
    
    parser.add_argument('input', nargs='?', help='Input image file, pattern, or directory')
    parser.add_argument('-o', '--output', help='Output PDF filename')
    parser.add_argument('-m', '--multi', help='Combine multiple images into single PDF')
    parser.add_argument('-d', '--directory', action='store_true', 
                       help='Convert all images in the input directory')
    parser.add_argument('-a4', '--resize-a4', action='store_true',
                       help='Resize images to A4 paper size')
    parser.add_argument('-q', '--quality', type=int, default=95,
                       help='Image quality (1-100, default: 95)')
    parser.add_argument('-l', '--list-formats', action='store_true',
                       help='List supported image formats')
    
    args = parser.parse_args()
    
    # List supported formats if requested
    if args.list_formats:
        print("Supported image formats:")
        for fmt in get_supported_formats():
            print(f"  {fmt}")
        return
    
    # If no input provided, show help
    if not args.input and not sys.argv[1:]:
        parser.print_help()
        
        # Offer interactive mode
        response = input("\n\nDo you want to use interactive mode? (y/n): ").strip().lower()
        if response == 'y':
            interactive_mode()
        return
    
    # Process based on arguments
    if args.directory and args.input:
        # Convert all images in directory
        input_path = Path(args.input)
        if input_path.is_dir():
            image_files = []
            for fmt in get_supported_formats():
                image_files.extend(input_path.glob(f'*{fmt}'))
                image_files.extend(input_path.glob(f'*{fmt.upper()}'))
            
            if not image_files:
                print(f"No supported images found in {args.input}")
                return
            
            print(f"Found {len(image_files)} images in directory")
            
            if args.multi:
                # Combine all into single PDF
                output_pdf = args.multi if args.multi else input_path / 'combined.pdf'
                convert_multiple_images_to_pdf(image_files, output_pdf, args.resize_a4, args.quality)
            else:
                # Convert each individually
                for img_file in image_files:
                    pdf_file = img_file.with_suffix('.pdf')
                    convert_image_to_pdf(img_file, pdf_file, args.resize_a4, args.quality)
        else:
            print(f"Error: {args.input} is not a directory")
    
    elif args.multi and args.input:
        # Handle glob patterns for multiple files
        image_files = sorted(glob.glob(args.input))
        
        if not image_files:
            print(f"No files found matching: {args.input}")
            return
        
        output_pdf = args.multi
        convert_multiple_images_to_pdf(image_files, output_pdf, args.resize_a4, args.quality)
    
    elif args.input:
        # Single file conversion
        input_path = Path(args.input)
        
        if not input_path.exists():
            print(f"Error: File not found: {args.input}")
            return
        
        output_pdf = args.output
        convert_image_to_pdf(args.input, output_pdf, args.resize_a4, args.quality)

def interactive_mode():
    """Interactive mode for user-friendly operation"""
    print("\n" + "="*50)
    print("Image to PDF Converter - Interactive Mode")
    print("="*50)
    
    while True:
        print("\nOptions:")
        print("1. Convert single image")
        print("2. Convert multiple images to individual PDFs")
        print("3. Combine multiple images into one PDF")
        print("4. Convert all images in a folder")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            img_path = input("Enter image path: ").strip()
            if img_path and Path(img_path).exists():
                output_name = input("Output PDF name (press Enter for auto-name): ").strip()
                output_name = output_name if output_name else None
                a4 = input("Resize to A4? (y/n): ").strip().lower() == 'y'
                convert_image_to_pdf(img_path, output_name, a4)
            else:
                print("File not found!")
        
        elif choice == '2':
            pattern = input("Enter image pattern (e.g., *.jpg): ").strip()
            image_files = sorted(glob.glob(pattern))
            
            if image_files:
                a4 = input("Resize to A4? (y/n): ").strip().lower() == 'y'
                for img_file in image_files:
                    convert_image_to_pdf(img_file, None, a4)
            else:
                print("No files found!")
        
        elif choice == '3':
            pattern = input("Enter image pattern (e.g., *.jpg): ").strip()
            image_files = sorted(glob.glob(pattern))
            
            if image_files:
                output_name = input("Output PDF name: ").strip()
                a4 = input("Resize to A4? (y/n): ").strip().lower() == 'y'
                convert_multiple_images_to_pdf(image_files, output_name, a4)
            else:
                print("No files found!")
        
        elif choice == '4':
            folder_path = input("Enter folder path: ").strip()
            folder = Path(folder_path)
            
            if folder.is_dir():
                option = input("Combine into single PDF or separate? (single/separate): ").strip().lower()
                a4 = input("Resize to A4? (y/n): ").strip().lower() == 'y'
                
                image_files = []
                for fmt in get_supported_formats():
                    image_files.extend(folder.glob(f'*{fmt}'))
                    image_files.extend(folder.glob(f'*{fmt.upper()}'))
                
                if image_files:
                    if option == 'single':
                        output_name = input("Output PDF name (press Enter for 'combined.pdf'): ").strip()
                        output_name = output_name if output_name else folder / 'combined.pdf'
                        convert_multiple_images_to_pdf(image_files, output_name, a4)
                    else:
                        for img_file in image_files:
                            convert_image_to_pdf(img_file, None, a4)
                else:
                    print("No images found in folder!")
            else:
                print("Folder not found!")
        
        elif choice == '5':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()