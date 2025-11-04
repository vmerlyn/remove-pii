import argparse
import sys
from pathlib import Path
import ocrmypdf

def main():
    parser = argparse.ArgumentParser(
        description='OCR PDF files using ocrmypdf',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input_file',
        type=str,
        help='Path to the input PDF file'
    )
    parser.add_argument(
        'output_file',
        type=str,
        help='Path to the output PDF file'
    )
    parser.add_argument(
        '--language',
        type=str,
        default='eng',
        help='Language code for OCR (ISO 639-2, e.g., eng, spa). Default: eng'
    )
    parser.add_argument(
        '--no-deskew',
        action='store_true',
        help='Disable deskew (fixing rotated scans)'
    )
    parser.add_argument(
        '--optimize',
        type=int,
        default=3,
        choices=[0, 1, 2, 3],
        help='Compression optimization level (0-3). Default: 3'
    )
    parser.add_argument(
        '--no-force-ocr',
        action='store_true',
        help='Disable force OCR (skip if text is detected)'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    
    # Ensure output directory exists
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Processing: {args.input_file} -> {args.output_file}")
    
    try:
        ocrmypdf.ocr(
            input_file=str(input_path),
            output_file=str(output_path),
            language=args.language,
            deskew=not args.no_deskew,
            optimize=args.optimize,
            force_ocr=not args.no_force_ocr
        )
        print(f"Successfully processed: {args.output_file}")
    except ocrmypdf.exceptions.PriorOcrFoundError:
        print("Error: PDF already contains OCR text. Use --no-force-ocr to skip.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing PDF: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()