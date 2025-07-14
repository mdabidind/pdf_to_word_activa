import os
import sys
import subprocess

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import streamlit
        import pdf2docx
        import PyPDF2
        from PIL import Image
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {str(e)}")
        print("Please install all required dependencies using: pip install -r requirements.txt")
        return False

def run_app(advanced=False):
    """Run the Streamlit application"""
    if not check_dependencies():
        return
    
    # Determine which app to run
    app_file = "advanced_app.py" if advanced else "app.py"
    
    try:
        print(f"Starting PDF to Word Converter {'(Advanced Mode)' if advanced else ''}...")
        print("The application will open in your default web browser.")
        print("Press Ctrl+C to stop the application.")
        
        # Run the Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_file])
    except KeyboardInterrupt:
        print("\nApplication stopped.")
    except Exception as e:
        print(f"❌ Error running the application: {str(e)}")

def main():
    # Check command line arguments
    advanced_mode = False
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["-a", "--advanced"]:
        advanced_mode = True
    
    # Run the app
    run_app(advanced_mode)

if __name__ == "__main__":
    main()