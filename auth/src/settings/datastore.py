from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from models import Role, User
from settings.database import db


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()


def init_datastore(app):
    security.init_app(app, user_datastore)


def init_datastore_commands(app: Flask):

    @app.cli.command()
    def init_roles():
        user_datastore.find_or_create_role(name='admin', description='Администратор')
        user_datastore.find_or_create_role(name='manager', description='Менеджер')
        user_datastore.find_or_create_role(name='user', description='Пользователь')
        db.session.commit()

    @app.cli.command()
    def init_admin():
        user = user_datastore.find_user(email='admin@admin.ru')
        if not user:
            user = user_datastore.create_user(
                email='admin@admin.ru',
                password='admin'
            )
            role = user_datastore.find_or_create_role(name='admin', description='Администратор')
            user.roles.append(role)
            db.session.commit()
