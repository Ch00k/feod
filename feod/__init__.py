from flask import Flask

ALLOWED_EXTENSIONS = set(['xls'])
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'test'
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://feod:feod@localhost/feod'
app.config['UPLOAD_FOLDER'] = '/var/tmp/'
app.secret_key = SECRET_KEY