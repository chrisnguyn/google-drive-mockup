import os
from auxiliary import *
from flask import Flask, redirect, render_template, request, Response, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO


# configure Flask application + SQLAlchemy database
app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)


# register URL routes
@app.route('/')
def index():
    user_query = request.args.get('user_tag')  # ie. '?user_tag=shopify'
    files = FileTable.query.all() if not user_query else FileTable.query.filter_by(tag=user_query)
    last_uploaded = FileTable.query.order_by('-id').first()
    tags = get_top_tags(files)

    return render_template('index.html', files=files, stats=tags, show=user_query==None, last=last_uploaded)


@app.route('/me')
def me():
    return render_template('me.html')


@app.route('/you')
def you():
    return render_template('you.html')


@app.route('/tag/')
def search_tag():
    user_query = request.args.get('user_tag')
    files = FileTable.query.filter(FileTable.tag.like(f'%{user_query}%')).all()

    if not user_query:
        return redirect(url_for('index'))

    return render_template('index.html', files=files)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    try:
        file = request.files['user_file']  # request.[type] for form data; get file from the form sent to server
        tags = clean_tags(request.form['user_caption']) or 'NO_TAG'
    except Exception as e:
        print(e)
        return render_template('error.html')

    database.session.add(FileTable(file.filename, tags, file.read()))
    database.session.commit()

    return redirect(url_for('index'))


@app.route('/retrieve/<id>')
def retrieve(id):
    file = FileTable.query.filter_by(id=id).first()

    if not file:
        return render_template('error.html')

    return send_file(BytesIO(file.file), attachment_filename=f'{file.name}')


@app.route('/delete/<id>')
def delete(id):
    file = FileTable.query.filter_by(id=id).first()

    if not file:
        return render_template('error.html')

    database.session.delete(file)
    database.session.commit()

    return redirect(url_for('index'))


@app.errorhandler(404)
def error(e):
    print(e)
    return render_template('error.html')


# configure database schema
class FileTable(database.Model):
    __tablename__ = 'USER_FILES'
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100))
    tag = database.Column(database.String(100))
    file = database.Column(database.LargeBinary)


    def __init__(self, name, tag, file):
        self.name = name
        self.tag = tag
        self.file = file


    def __repr__(self):
        return f'FILE ID: {self.id} \n FILE NAME: {self.name} \n FILE TAG: {self.tag} \n'


# reset database, populate wtih some dummy data
database.drop_all()
database.create_all()

image_1 = open('src/static/media/awesome_image.jpg', 'rb').read()
image_2 = open('src/static/media/king_of_shopify.jpg', 'rb').read()
image_3 = open('src/static/media/cool_image.jpg', 'rb').read()
image_4 = open('src/static/media/hello_world.jpg', 'rb').read()
image_5 = open('src/static/media/shopify_hire_me_please.jpg', 'rb').read()
image_6 = open('src/static/media/resume.pdf', 'rb').read()
image_7 = open('src/static/media/designdocument.pdf', 'rb').read()

dummy_1 = FileTable('awesome_image.jpg', 'hi', image_1)
dummy_2 = FileTable('king_of_shopify.jpg', 'tobi', image_2)
dummy_3 = FileTable('cool_image.jpg', 'hire', image_3)
dummy_4 = FileTable('hello_world.jpg', 'me', image_4)
dummy_5 = FileTable('shopify_hire_me_please.jpg', 'please', image_5)
dummy_6 = FileTable('my_resume.pdf', 'my resume', image_6)
dummy_7 = FileTable('how_this_was_built.pdf', 'design document', image_7)

database.session.add_all([dummy_1, dummy_2, dummy_3, dummy_4, dummy_5, dummy_6, dummy_7])
database.session.commit()


if __name__ == '__main__':
    print('\n###########################################################################')
    print('\n\nFile Repository Backend Challenge - made with love by Christopher Nguyen :)\n\n')
    print('###########################################################################\n')
    app.run(host='0.0.0.0')
