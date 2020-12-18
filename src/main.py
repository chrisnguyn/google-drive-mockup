import os
from flask import Flask, redirect, render_template, request, Response, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO


# configure Flask application + SQLAlchemy database
app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)


# configure database schema
class FileTable(database.Model):
    __tablename__ = 'uploaded_files'
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
dummy_6 = FileTable('heres_my_resume.pdf', 'chris resume', image_6)
dummy_7 = FileTable('heres_how_i_built_this.pdf', 'design document', image_7)

database.session.add_all([dummy_1, dummy_2, dummy_3, dummy_4, dummy_5, dummy_6, dummy_7])
database.session.commit()


# register URL routes
# main page
@app.route('/')
def index():
    user_tag = request.args.get('user_tag')  # what files should I show? tags don't show if user is filtering

    if user_tag:
        files = FileTable.query.filter_by(tag=user_tag)
        show_tags = False
    else:
        files = FileTable.query.all()
        show_tags = True

    tags = {}  # your top 3 tags
    for file in files:
        for tag in file.tag.split(' '):
            if tag == 'NO_TAG':
                continue
            elif tag not in tags:
                tags[tag] = 0
            tags[tag] += 1
    sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)

    last_uploaded = FileTable.query.order_by('-id').first()  # last uploaded file

    return render_template('index.html', files=files, stats=sorted_tags, show=show_tags, last=last_uploaded)


# about me page
@app.route('/me')
def me():
    return render_template('me.html')


# about 'you' page
@app.route('/you')
def you():
    return render_template('you.html')


# if user is searching by specific tags
@app.route('/tag/')
def search_tag():
    user_tag = request.args.get('user_tag')  # ie. '?user_tag=shopify'
    search = f'%{user_tag}%'
    files = FileTable.query.filter(FileTable.tag.like(search)).all()

    if len(user_tag) == 0:
        return redirect(url_for('index'))

    return render_template('index.html', files=files, last='REDIRECTFROMTAG')


# upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        try:
            request.files['user_file']
        except Exception as e:
            return render_template('error.html')

        file = request.files['user_file']  # use request.[type] for FORM DATA; get file from form sent to server
        tag = request.form['user_caption']  # get tag sent from form sent to server (if it exists)

        if not tag:
            tag = 'NO_TAG'

        database.session.add(FileTable(file.filename, tag, file.read()))
        database.session.commit()

        return redirect(url_for('index'))


# opening a file that was uploaded to database
@app.route('/retrieve/<id>')
def retrieve(id):
    file = FileTable.query.filter_by(id=id).first()

    if not file:
        return render_template('error.html')

    data = BytesIO(file.file)
    return send_file(data, attachment_filename=f'{file.name}')


# deleting a file
@app.route('/delete/<id>')
def delete(id):
    file = FileTable.query.filter_by(id=id).first()

    if not file:
        return render_template('error.html')

    database.session.delete(file)
    database.session.commit()
    return redirect(url_for('index'))


# visiting an unregistered route
@app.errorhandler(404)
def error(e):
    return render_template('error.html')


if __name__ == "__main__":
    print('\n#########################')
    print('\n\nFile Repository Backend Challenge - made with love by Christopher Nguyen :)\n\n')
    print('#########################\n')
    app.run(host='0.0.0.0')
