from flask import Flask, render_template, request, redirect
import os
from nbconvert import HTMLExporter
import nbformat

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'ipynb'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Convert notebook to HTML
        html_exporter = HTMLExporter()
        nb_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        notebook = nbformat.read(nb_path, as_version=4)
        (html, _) = html_exporter.from_notebook_node(notebook)

        # Remove the uploaded .ipynb file
        os.remove(file_path)

        # Render the HTML in the template
        return render_template('index.html', notebook_html=html)

    return redirect(request.url)

'''if __name__ == '__main__':
    app.run(debug=True)
'''
