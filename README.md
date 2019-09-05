# GetGettyFlaskApp
A small application for downloading high quality images *without watermark* from some popular photo hosting.

Be aware: images may be copyrighted. In this case, you cannot use them without permission from the owner.

### Used with Chrome extension: https://github.com/Dreyk007/GetGettyChromeExtension

## How to run:

### Install dependencies using pip:
* flask
* flask-wtf
* flask-sqlalchemy
* flask-login
* flask-bootstrap
* flask-migrate
* requests
* Pillow

### In the command line:
* git clone https://github.com/Dreyk007/GetGettyFlaskApp.git
* cd GetGettyFlaskApp
* export FLASK_APP=GetGetty.py
* flask db upgrade
* flask run

### In the browser:
* Open http://127.0.0.1:5000/
* Sign up and login
* Get your token to insert into the "GetGetty" Chrome extension settings

### Notes:
* Basic Views related to registration and authorization are in the: GetGettyFlaskApp/app/routes.py
* The View for verifying api key and downloading images is in the GetGettyFlaskApp/app/api.py
* Logic of image processing in the: GetGettyFlaskApp/GetGettyDownloader.py

## Use for educational purposes only.
