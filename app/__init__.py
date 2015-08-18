import os
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from config import basedir
import filters



# The Flask application
app = Flask(__name__)
app.config.from_object('config')

# Flask Login Manager
lm = LoginManager()
lm.session_protection = 'basic'
lm.init_app(app)
lm.login_view = 'login'


# Custom jinja filters
app.jinja_env.filters['epoch'] = filters.jinja2_filter_formatepoch
app.jinja_env.filters['epochdate'] = filters.jinja2_filter_formatepochdate
app.jinja_env.filters['epochshort'] = filters.jinja2_filter_formatepochshort
app.jinja_env.filters['epochrange'] = filters.jinja2_filter_formatepochrange
app.jinja_env.add_extension('jinja2.ext.do')

# Database Connection
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Views These need to be after the db
from app import views
from app import ajax_views


# Manager (Command Line) commands
manager = Manager(app)
manager.add_command('db', MigrateCommand)



# Email Error Messages
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    if app.config['PYTHON_LOG']:
        file_handler = RotatingFileHandler(app.config['PYTHON_LOG'], maxBytes=1024 * 1024 * 100, backupCount=20)
        file_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
    