
import os
import shutil

from app import app

from werkzeug.utils import secure_filename
from flask import flash, request, redirect, url_for, render_template

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    text = request.form['text']
    print(text)
    aa = app.config['UPLOAD_FOLDER']
    role = request.form['role']
    uploadFolder = aa+'cdgs'+'/'+role+'/'
    name = request.form['name']
    surname = request.form['surname']
    code = request.form['code']
    full = name+" "+surname+" "+code
    ab = uploadFolder+full
    os.mkdir(ab)
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(ab, filename))
    # os.system('python D:/pythonProject2/2.py --dataset data --encodings encodings.pickle')
    # else:
    # flash('Allowed image types are -> png, jpg, jpeg, gif')
    # return redirect(request.url)

    src = ab
    dest = 'static/output'
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dest)
    os.system('python encode.py --dataset data2 --encodings encodings.pickle')
    return render_template('upload.html', filenames=file_names)


@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)

    return redirect(url_for('static', filename='output/' + filename), code=301)


if __name__ == "__main__":
    app.run()
#git remote add origin https://github.com/markkapoom/web_face.git venv