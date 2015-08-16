import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess2'
PASSWORD_SALT = os.environ.get('PASSWORD_SALT', 'xxxxxx')

PYTHON_LOG = os.environ.get('PYTHON_LOG', '')

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'app.db'))

PHOTO_PATH = os.environ.get('PHOTO_PATH', 'app/static/photos')

SMTP_HOST   = os.environ.get('SMTP_HOST', 'smtp.gmail.com:587')
SMTP_USER   = os.environ.get('SMTP_USER', '')
SMTP_PASSWD = os.environ.get('SMTP_PASSWD', '')

ADMINS = ['nicka@axcella.com']
