from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()


class ConfigDatabase:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:280124@localhost/classOn'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
