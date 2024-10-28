from flask import Flask, request, render_template_string
import fitz  # PyMuPDF
from ebooklib import epub

app = Flask(__name__)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to extract text from EPUB
def extract_text_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    text = ""
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text += item.get_body_content_str()
    return text

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.filename.endswith('.epub'):
            text = extract_text_from_epub(uploaded_file)
        else:
            return "Invalid file type. Please upload a PDF or EPUB file."
        
        return render_template_string(RETYPE_HTML, text=text)
    
    return render_template_string(UPLOAD_HTML)

UPLOAD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Book</title>
</head>
<body>
    <h1>Upload PDF or EPUB</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Upload</button>
    </form>
</body>
</html>
'''

RETYPE_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retype Text</title>
</head>
<body>
    <h1>Retype the Text Below</h1>
    <form method="post" action="/retype">
        <textarea name="user_input" rows="10" cols="50" required>{{ text }}</textarea>
        <input type="hidden" name="original_text" value="{{ text }}">
        <button type="submit">Submit</button>
    </form>
</body>
</html>
'''

@app.route('/retype', methods=['POST'])
def retype_text():
    user_input = request.form['user_input']
    original_text = request.form['original_text']
    return "Your retyped text: <br><pre>{}</pre>".format(user_input)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
