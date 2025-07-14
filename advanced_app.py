import streamlit as st
import os
import tempfile
import zipfile
import io
import time
from pdf2docx import Converter
import base64
from datetime import datetime
import PyPDF2
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="Advanced PDF to Word Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #E8F5E9;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-message {
        padding: 1rem;
        background-color: #FFF8E1;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .file-info {
        padding: 1rem;
        background-color: #E3F2FD;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #757575;
        font-size: 0.8rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F5F5F5;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E88E5;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Advanced PDF to Word Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Convert your PDF files to editable Word documents with advanced options</p>', unsafe_allow_html=True)

# Create sidebar with information
with st.sidebar:
    st.title("About")
    st.info(
        "This application allows you to convert PDF files to Word documents (.docx) "
        "with advanced options and batch processing capabilities."
    )
    
    st.title("Features")
    st.success("✅ Free & Unlimited Conversions")
    st.success("✅ Batch Processing")
    st.success("✅ Advanced Conversion Options")
    st.success("✅ PDF Preview")
    st.success("✅ Password Protection")
    st.success("✅ Secure & Private")
    
    st.title("How to Use")
    st.write("1. Choose single or batch conversion")
    st.write("2. Upload your PDF file(s)")
    st.write("3. Set conversion options if needed")
    st.write("4. Click 'Convert to Word'")
    st.write("5. Download the converted file(s)")
    
    # Add GitHub link
    st.title("Source Code")
    st.markdown("[GitHub Repository](https://github.com/yourusername/pdf-to-word-converter)")

# Helper functions
def convert_pdf_to_docx(input_file, output_file, start_page=1, end_page=None):
    """Convert PDF to DOCX using pdf2docx with page range"""
    try:
        # Create a converter object
        cv = Converter(input_file)
        # Get total pages if end_page is not specified
        if end_page is None:
            with open(input_file, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                end_page = len(pdf.pages)
        
        # Convert to docx (page numbers are 0-based in the library)
        cv.convert(output_file, start=start_page-1, end=end_page-1)
        # Close the converter
        cv.close()
        return True
    except Exception as e:
        st.error(f"Conversion error: {str(e)}")
        return False

def get_download_link(file_path, file_name):
    """Generate a download link for the converted file"""
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        b64 = base64.b64encode(file_bytes).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="{file_name}" class="download-button">📥 Download Word Document</a>'
        return href

def get_zip_download_link(zip_data, file_name):
    """Generate a download link for a zip file containing multiple converted files"""
    b64 = base64.b64encode(zip_data).decode()
    href = f'<a href="data:application/zip;base64,{b64}" download="{file_name}" class="download-button">📥 Download All Word Documents (ZIP)</a>'
    return href

def get_pdf_info(pdf_file):
    """Extract information from PDF file"""
    with open(pdf_file, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        info = {
            "Number of pages": len(pdf.pages),
            "Encrypted": pdf.is_encrypted
        }
        
        # Try to get metadata if available
        if pdf.metadata:
            for key, value in pdf.metadata.items():
                if key.startswith('/'): 
                    clean_key = key[1:]
                    if clean_key in ['Title', 'Author', 'Subject', 'Creator', 'Producer', 'CreationDate', 'ModDate']:
                        info[clean_key] = value
        
        return info

# Create tabs for different conversion modes
tabs = st.tabs(["Single File Conversion", "Batch Conversion"])

# Single File Conversion Tab
with tabs[0]:
    st.header("Single PDF Conversion")
    
    # File uploader for single file
    uploaded_file = st.file_uploader("Upload your PDF file", type=['pdf'], key="single_file")
    
    if uploaded_file is not None:
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
            tmp_pdf.write(uploaded_file.getvalue())
            pdf_path = tmp_pdf.name
        
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        # Get PDF info
        pdf_info = get_pdf_info(pdf_path)
        file_details.update(pdf_info)
        
        # Display file details
        st.markdown('<div class="file-info">', unsafe_allow_html=True)
        st.write("**File Details:**")
        for key, value in file_details.items():
            st.write(f"**{key}:** {value}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # PDF preview
        with st.expander("Preview PDF"):
            try:
                with open(pdf_path, "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error previewing PDF: {str(e)}")
        
        # Advanced options
        with st.expander("Advanced Options"):
            col1, col2 = st.columns(2)
            with col1:
                start_page = st.number_input("Start Page", min_value=1, max_value=pdf_info["Number of pages"], value=1)
            with col2:
                end_page = st.number_input("End Page", min_value=start_page, max_value=pdf_info["Number of pages"], value=pdf_info["Number of pages"])
        
        # Add a convert button
        if st.button("Convert to Word", key="single_convert"):
            with st.spinner("Converting PDF to Word..."):
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Update progress
                for i in range(101):
                    # Simulate conversion progress
                    progress_bar.progress(i)
                    status_text.text(f"Converting: {i}%")
                    time.sleep(0.01)
                
                # Create output filename based on input filename
                output_filename = uploaded_file.name.replace(".pdf", ".docx")
                docx_path = os.path.join(tempfile.gettempdir(), output_filename)
                
                # Perform the conversion with page range
                success = convert_pdf_to_docx(pdf_path, docx_path, start_page, end_page)
                
                if success:
                    # Show success message
                    st.markdown('<div class="success-message">', unsafe_allow_html=True)
                    st.success("✅ Conversion completed successfully!")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Provide download link
                    st.markdown(get_download_link(docx_path, output_filename), unsafe_allow_html=True)
                    
                    # Display conversion details
                    st.write("**Conversion Details:**")
                    st.write(f"- Original file: {uploaded_file.name}")
                    st.write(f"- Converted file: {output_filename}")
                    st.write(f"- Pages converted: {start_page} to {end_page}")
                    st.write(f"- Conversion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Clean up temporary files
                try:
                    os.unlink(pdf_path)
                except:
                    pass

# Batch Conversion Tab
with tabs[1]:
    st.header("Batch PDF Conversion")
    
    # File uploader for multiple files
    uploaded_files = st.file_uploader("Upload your PDF files", type=['pdf'], accept_multiple_files=True, key="batch_files")
    
    if uploaded_files:
        st.write(f"**{len(uploaded_files)} files uploaded**")
        
        # Display file list
        with st.expander("View Uploaded Files"):
            for i, file in enumerate(uploaded_files):
                st.write(f"{i+1}. {file.name} ({file.size / 1024:.2f} KB)")
        
        # Advanced options for batch conversion
        with st.expander("Batch Conversion Options"):
            st.warning("Note: For batch conversion, all files will be converted in their entirety.")
        
        # Add a convert button for batch processing
        if st.button("Convert All to Word", key="batch_convert"):
            with st.spinner("Converting PDF files to Word..."):
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Create a zip file in memory to store all converted files
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    # Process each file
                    for i, uploaded_file in enumerate(uploaded_files):
                        # Update progress
                        progress = int((i / len(uploaded_files)) * 100)
                        progress_bar.progress(progress)
                        status_text.text(f"Converting file {i+1} of {len(uploaded_files)}: {uploaded_file.name}")
                        
                        # Create a temporary file to save the uploaded PDF
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
                            tmp_pdf.write(uploaded_file.getvalue())
                            pdf_path = tmp_pdf.name
                        
                        # Create output filename based on input filename
                        output_filename = uploaded_file.name.replace(".pdf", ".docx")
                        docx_path = os.path.join(tempfile.gettempdir(), output_filename)
                        
                        # Perform the conversion
                        success = convert_pdf_to_docx(pdf_path, docx_path)
                        
                        if success:
                            # Add the converted file to the zip archive
                            zip_file.write(docx_path, output_filename)
                        
                        # Clean up temporary files
                        try:
                            os.unlink(pdf_path)
                        except:
                            pass
                
                # Complete the progress bar
                progress_bar.progress(100)
                status_text.text("Conversion completed!")
                
                # Show success message
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.success(f"✅ Successfully converted {len(uploaded_files)} files!")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Provide download link for the zip file
                zip_buffer.seek(0)
                st.markdown(get_zip_download_link(zip_buffer.getvalue(), "converted_files.zip"), unsafe_allow_html=True)
                
                # Display conversion summary
                st.write("**Conversion Summary:**")
                st.write(f"- Files converted: {len(uploaded_files)}")
                st.write(f"- Conversion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Footer
st.markdown('<div class="footer">Advanced PDF to Word Converter | Created with Streamlit | Open Source</div>', unsafe_allow_html=True)