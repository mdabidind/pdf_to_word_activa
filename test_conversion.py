import os
import tempfile
from pdf2docx import Converter
import sys

def test_conversion(pdf_path):
    """Test PDF to DOCX conversion with a sample file"""
    try:
        # Create output path
        output_path = pdf_path.replace('.pdf', '_converted.docx')
        
        # Create a converter object
        cv = Converter(pdf_path)
        
        # Convert to docx
        cv.convert(output_path)
        
        # Close the converter
        cv.close()
        
        # Check if the output file exists
        if os.path.exists(output_path):
            print(f"✅ Conversion successful! Output file: {output_path}")
            return True
        else:
            print(f"❌ Conversion failed: Output file not found")
            return False
    except Exception as e:
        print(f"❌ Conversion error: {str(e)}")
        return False

def main():
    # Check if a PDF file path is provided as an argument
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        if not os.path.exists(pdf_path):
            print(f"❌ Error: File '{pdf_path}' not found")
            return
        
        # Test the conversion
        test_conversion(pdf_path)
    else:
        print("❌ Error: Please provide a PDF file path as an argument")
        print("Usage: python test_conversion.py path/to/your/file.pdf")

if __name__ == "__main__":
    main()