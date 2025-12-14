from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from authlib.integrations.flask_client import OAuth  # OAuth client for third-party authentication
from flask_login import LoginManager    
from config import Config
from flask_moment import Moment
from dotenv import find_dotenv, load_dotenv
from os import environ as env                     # Access environment variables
from authlib.integrations.flask_client import OAuth

import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

db = SQLAlchemy()

migrate = Migrate()
moment = Moment()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER_SRC

    db.init_app(app)
    migrate.init_app(app,db)
    moment.init_app(app)
    # register blueprints

    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

    from app.src import src_blueprint as src
    src.template_folder = Config.TEMPLATE_FOLDER_SRC
    app.register_blueprint(src)

    from app.errors import error_blueprint as errors
    errors.template_folder = Config.TEMPLATE_FOLDER_ERRORS
    app.register_blueprint(errors)

    return app