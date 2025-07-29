from flask import Flask, request, send_file, render_template
import os
import uuid
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('pdf_to_word.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'pdfFile' not in request.files:
        return 'No file uploaded', 400

    file = request.files['pdfFile']
    if not file.filename.lower().endswith('.pdf'):
        return 'Only PDF files are allowed', 400

    # Save uploaded PDF
    uid = str(uuid.uuid4())
    pdf_path = os.path.join(UPLOAD_FOLDER, f"{uid}.pdf")
    docx_path = os.path.join(UPLOAD_FOLDER, f"{uid}.docx")
    file.save(pdf_path)

    try:
        result = subprocess.run(
            ['python3', 'convert_pdf_to_docx.py', pdf_path, docx_path],
            capture_output=True,
            text=True,
            timeout=120
        )

        if 'success' in result.stdout.lower():
            return send_file(docx_path, as_attachment=True)
        else:
            print("Conversion stdout:", result.stdout)
            print("Conversion stderr:", result.stderr)
            return f"Conversion failed: {result.stdout or result.stderr}", 500

    except Exception as e:
        return f"Server error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
