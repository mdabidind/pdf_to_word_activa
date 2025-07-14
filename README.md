# PDF to Word Converter

A free, open-source tool to convert PDF files to editable Word documents (.docx) with a clean and user-friendly web interface.

## Features

- ✅ **Free & Unlimited Conversions**: No restrictions on file size or number of conversions
- ✅ **Preserves Formatting**: Maintains text formatting, images, and tables
- ✅ **No Registration Required**: Just upload and convert
- ✅ **Secure & Private**: Files are processed locally and not stored on any server
- ✅ **Open Source**: Free to use, modify, and distribute

## Demo

You can try the live demo of this application on [Streamlit Community Cloud](https://streamlit.io/cloud).

## How to Use

1. Upload your PDF file using the file uploader
2. Click the "Convert to Word" button
3. Download the converted Word document

## Installation and Local Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pdf-to-word-converter.git
   cd pdf-to-word-converter
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. Open your web browser and go to `http://localhost:8501`

## Deployment

### Deploy on Streamlit Community Cloud (Free)

1. Fork this repository to your GitHub account
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click on "New app"
5. Select the repository, branch, and file path (app.py)
6. Click "Deploy"

### Deploy on GitHub Pages (Alternative)

To deploy this application on GitHub Pages, you'll need to use Streamlit's static export feature with Streamlit-Components-Template:

1. Install the required packages:
   ```bash
   pip install streamlit-components-template
   ```

2. Create a GitHub workflow file in `.github/workflows/deploy.yml` with the deployment configuration

3. Push your changes to GitHub and enable GitHub Pages in your repository settings

## How It Works

This application uses the following libraries:

- **Streamlit**: For the web interface
- **pdf2docx**: For converting PDF files to Word documents
- **PyPDF2**: For reading PDF metadata
- **python-docx**: For handling Word documents

The conversion process preserves text formatting, images, tables, and other elements from the original PDF file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [pdf2docx](https://github.com/dothinking/pdf2docx) for the PDF to Word conversion functionality