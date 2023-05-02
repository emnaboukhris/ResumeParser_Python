from flask import Flask, request
import os


app = Flask(__name__)

UPLOAD_FOLDER = '/resume'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Check if the file was uploaded
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    # Save the file to the upload folder
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return 'File uploaded successfully', 200


if __name__ == '__main__':
    app.run()
