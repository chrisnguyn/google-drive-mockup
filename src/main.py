import os
from collections import Counter
from flask import Flask, redirect, render_template, request, Response, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO


# configure Flask application + SQLAlchemy database
app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)


# setup database schema
class FileTable(database.Model):
    __tablename__ = 'user_files'
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


# reset database, add some dummy data
database.drop_all()
database.create_all()

file_open = open('src/static/media/awesome_image.jpg', 'rb')
image_1 = file_open.read()
file_open.close()
file_open = open('src/static/media/king_of_shopify.jpg', 'rb')
image_2 = file_open.read()
file_open.close()
file_open = open('src/static/media/cool_image.jpg', 'rb')
image_3 = file_open.read()
file_open.close()
file_open = open('src/static/media/hello_world.jpg', 'rb')
image_4 = file_open.read()
file_open.close()
file_open = open('src/static/media/shopify_hire_me_please.jpg', 'rb')
image_5 = file_open.read()
file_open.close()
file_open = open('src/static/media/resume.pdf', 'rb')
image_6 = file_open.read()
file_open.close()

dummy_input_1 = FileTable('awesome_image.jpg', 'hi', image_1)
dummy_input_2 = FileTable('king_of_shopify.jpg', 'tobi', image_2)
dummy_input_3 = FileTable('cool_image.jpg', 'hire', image_3)
dummy_input_4 = FileTable('hello_world.jpg', 'me', image_4)
dummy_input_5 = FileTable('shopify_hire_me_please.jpg', 'please', image_5)
dummy_input_6 = FileTable('heres_my_resume.pdf', 'chris resume', image_6)

database.session.add_all([dummy_input_1, dummy_input_2, dummy_input_3, dummy_input_4, dummy_input_5, dummy_input_6])
database.session.commit()


# register URL routes
@app.route('/')
def index():
    user_tag = request.args.get('user_tag')  # user request.args.get() for QUERY STRING PARAMETERS

    if user_tag:
        files = FileTable.query.filter_by(tag=user_tag)
        show_tags = False
    else:
        files = FileTable.query.all()
        show_tags = True

    tags = {}
    for file in files:
        for x in file.tag.split(' '):
            if x == 'NO_TAG':
                continue
            elif x not in tags:
                tags[x] = 0
            tags[x] += 1
    sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)

    last_uploaded = FileTable.query.order_by('-id').first()

    return render_template('index.html', files=files, stats=sorted_tags, show=show_tags, last=last_uploaded)


@app.route('/me')
def me():
    return render_template('me.html')


@app.route('/you')
def you():
    return render_template('you.html')


@app.route('/tag/')
def search_tag():
    user_tag = request.args.get('user_tag')  # i.e. '?user_tag=shopify', requesting user_tag gives the value to this key
    search = f'%{user_tag}%'  # https://stackoverflow.com/questions/3325467/sqlalchemy-equivalent-to-sql-like-statement
    files = FileTable.query.filter(FileTable.tag.like(search)).all()

    if len(user_tag) == 0:
        return redirect(url_for('index'))

    return render_template('index.html', files=files, last='REDIRECTFROMTAG')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':  # if user visits this page manually (GET) then return default page
        return render_template('upload.html')
    elif request.method == 'POST':  # if user visits this page through uploading a file (POST) submit it to database
        try:
            request.files['user_file']
        except Exception as e:
            return render_template('error.html')

        file = request.files['user_file']  # use request.[type] for FORM DATA; get file from form sent to server
        tag = request.form['user_caption']  # get tag sent from form sent to server (if it exists), tag can be 'chris,nguyen,shopify' - delimited by commas

        if not tag:
            tag = 'NO_TAG'

        database.session.add(FileTable(file.filename, tag, file.read()))
        database.session.commit()

        return redirect(url_for('index'))


@app.route('/retrieve/<id>')
def retrieve(id):
    file = FileTable.query.filter_by(id=id).first()

    if not file:
        return render_template('error.html')

    data = BytesIO(file.file)
    return send_file(data, attachment_filename=f'{file.name}')


@app.route('/delete/<id>')  # you can delete just by visiting the endpoint which isn't great but I'm too tired for this
def delete(id):
    file = FileTable.query.filter_by(id=id).first()

    if not file:
        return render_template('error.html')

    database.session.delete(file)
    database.session.commit()
    return redirect(url_for('index'))  # url_for generates the link, redirect actually goes to it


@app.errorhandler(404)
def error(e):
    return render_template('error.html')


if __name__ == "__main__":
    print('\n#########################')
    print('\n\nFile Repository Backend Challenge - made with love by Christopher Nguyen :)\n\n')
    print('#########################\n')
    app.run(debug=True, host='0.0.0.0')
