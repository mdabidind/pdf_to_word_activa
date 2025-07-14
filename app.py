import streamlit as st
import os
import tempfile
from pdf2docx import Converter
import base64
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="PDF to Word Converter",
    page_icon="📄",
    layout="centered",
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">PDF to Word Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Convert your PDF files to editable Word documents instantly</p>', unsafe_allow_html=True)

# Create sidebar with information
with st.sidebar:
    st.title("About")
    st.info(
        "This application allows you to convert PDF files to Word documents (.docx) "
        "without any limitations. Upload your PDF, convert it, and download the result."
    )
    
    st.title("Features")
    st.success("✅ Free & Unlimited Conversions")
    st.success("✅ Preserves Text Formatting")
    st.success("✅ Maintains Images & Tables")
    st.success("✅ No Registration Required")
    st.success("✅ Secure & Private")
    
    st.title("How to Use")
    st.write("1. Upload your PDF file")
    st.write("2. Click 'Convert to Word'")
    st.write("3. Download the converted file")

# File uploader
uploaded_file = st.file_uploader("Upload your PDF file", type=['pdf'])

def convert_pdf_to_docx(input_file, output_file):
    """Convert PDF to DOCX using pdf2docx"""
    try:
        # Create a converter object
        cv = Converter(input_file)
        # Convert to docx
        cv.convert(output_file)
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

# Main conversion process
if uploaded_file is not None:
    # Display file info
    file_details = {
        "Filename": uploaded_file.name,
        "File size": f"{uploaded_file.size / 1024:.2f} KB"
    }
    
    st.markdown('<div class="file-info">', unsafe_allow_html=True)
    st.write("**File Details:**")
    for key, value in file_details.items():
        st.write(f"**{key}:** {value}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add a convert button
    if st.button("Convert to Word"):
        with st.spinner("Converting PDF to Word..."):
            # Create temporary files for processing
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
                tmp_pdf.write(uploaded_file.getvalue())
                pdf_path = tmp_pdf.name
            
            # Create output filename based on input filename
            output_filename = uploaded_file.name.replace(".pdf", ".docx")
            docx_path = os.path.join(tempfile.gettempdir(), output_filename)
            
            # Perform the conversion
            success = convert_pdf_to_docx(pdf_path, docx_path)
            
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
                st.write(f"- Conversion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Clean up temporary files
            try:
                os.unlink(pdf_path)
            except:
                pass

# Footer
st.markdown('<div class="footer">PDF to Word Converter | Created with Streamlit | Open Source</div>', unsafe_allow_html=True)