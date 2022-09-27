from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from helpers.utility import backoff


db = SQLAlchemy()
migrate = Migrate()


@backoff()
def init_db(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
