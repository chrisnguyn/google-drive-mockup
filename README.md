# Shopify Summer 2021 Backend Challenge <img src="https://github.com/chrisngyn/chrisngyn/blob/master/Hi.gif" width="30px">

## Abstract
This is a file repository project created for Shopify's summer 2021 backend developer intern challenge. This user is able to upload and view files, attach optional 'tags' to photos, and can filter files by their respective tags. Supports images, documents, even video files!

This project is made with HTML + CSS + JS + Bootstrap for the frontend, Python + Flask for the backend, a SQLite database to store images, and SQLAlchemy as the ORM.

*pls hire me @Shopify*

<p align="center"><img src="https://github.com/chrisngyn/shopify-file-repo/blob/main/src/static/media/demo.gif" width="80%"></p>

## Configuration
You can run this project in one of two ways.

**With Docker**

1. Clone the repository to your machine

       $ git clone https://github.com/chrisngyn/shopify-file-repo.git
       
2. Change into the directory

       $ cd shopify-file-repository

3. After turning on Docker, run this command first

       $ docker build -t file-repo .

4. After that command has completed, run this command next

       $ docker run -p 80:5000 --name shopify-file-repo file-repo

5. The server should now be started, navigate to `http://localhost/` in your browser and enjoy!

**Without Docker**

1. It is recommended you send up a virtual environment (but completely optional)
       
       $ virtualenv env
       $ source env/bin/activate

2. Install dependencies

       $ pip3 install setuptools==45
       $ pip3 install -r requirements.txt

1. Start the server (be in the root directory, not in `src/`)

       $ python3 src/main.py
       
2. The server should now be started, navigate to `http://localhost:5000` in your browser and enjoy!


3. Note - if on Windows and not using Docker, you may need to go into `src/main.py` and change `app.run(host='0.0.0.0')` to `app.run(host='127.0.0.1')` (I develop on a Mac and it's works fine, but my friends stress tested this for me and it's a little wonky on their Windows machines!)


## Future Improvements
There are several things I would like to add onto this project in the future should I keep working on this, namely:

1. User authentication (be able register with an email / password)
2. Suggested tags with image recognition on uploading files (using OpenCV)
3. Have ephemeral based file sharing sessions with friends (using some socket magic)
4. Use lightbox to open images from the main page instead of opening it in a new tab


## Miscellaneous
I documented a lot of the process in making this project in a design document which you can view [here](https://github.com/chrisngyn/shopify-file-repo/blob/main/src/static/media/designdocument.pdf).

This project was made with much love by Christopher Nguyen :heart:
