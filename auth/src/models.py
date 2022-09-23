from datetime import timedelta

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_security import RoleMixin, UserMixin
from flask_security.utils import hash_password
from marshmallow import ValidationError
from settings.config import configuration
from settings.database import db
from sqlalchemy.orm import validates


class QuerysetMixin(db.Model):
    __abstract__ = True

    pk = db.Column(db.Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get_by_pk(cls, pk):
        return cls.query.filter_by(pk=pk).first()

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class TimestampMixin:
    __abstract__ = True

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )


roles_users = db.Table('roles_users',
                       db.Column('user_pk', db.Integer(), db.ForeignKey('users.pk')),
                       db.Column('role_pk', db.Integer(), db.ForeignKey('roles.pk')))


class Role(TimestampMixin, RoleMixin, QuerysetMixin):
    __tablename__ = 'roles'

    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Role #{self.pk} {self.name}>'

    @validates('name')
    def validate_name(self, key, name):
        role_exist = self.query.filter_by(name=name).first()
        if role_exist and self.pk != role_exist.pk:
            raise ValidationError([f'Role with name "{name}" exist'], field_name=key)
        if name.isdigit():
            raise ValidationError([f'Incorrect role name: {name}'], field_name=key)
        return name

    @classmethod
    def get_by_name(cls, name):
        instance = cls.query.filter_by(name=name).first()
        if not instance:
            raise ValidationError([f'Role with name "{name}" does not exist'], field_name='name')
        return instance


class User(TimestampMixin, UserMixin, QuerysetMixin):
    __tablename__ = 'users'

    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(150))
    birth_date = db.Column(db.Date)
    phone = db.Column(db.String(255), index=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('Role',
                            secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = hash_password(kwargs.get('password'))

    def __repr__(self):
        return f'<User - {self.get_full_name()}>'

    @validates('email')
    def validate_email(self, key, email):
        user_exist = self.query.filter_by(email=email).first()
        if user_exist and self.pk != user_exist.pk:
            raise ValidationError([f'User with email "{email}" already exists'], field_name=key)
        return email

    def get_full_name(self):
        full_name = ' '.join(filter(None, [self.first_name, self.last_name])).strip()
        return full_name or self.email

    def get_jwt_token(self, expire_time: int = configuration.ACCESS_TOKEN_EXPIRE_TIME):
        expire_time = timedelta(seconds=expire_time)
        access_token = create_access_token(identity=self.pk, expires_delta=expire_time)
        refresh_token = create_refresh_token(identity=self.pk, expires_delta=(expire_time * 24))
        return dict(access_token=access_token, refresh_token=refresh_token)

    def add_role(self, role, security):
        security.datastore.add_role_to_user(self, role)
        db.session.commit()

    def delete_role(self, role, security):
        security.datastore.remove_role_from_user(self, role)
        db.session.commit()


class UserSessions(QuerysetMixin):
    __tablename__ = 'user_sessions'
    __table_args__ = (
        db.UniqueConstraint('pk', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
        }
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.pk'), nullable=False)
    user_agent = db.Column(db.Text, nullable=False)
    last_login = db.Column(db.DateTime(timezone=True), nullable=False)
    user_device_type = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return f'<UserSignIn {self.user_id}:{self.last_login}>'


class UserOauthServices(QuerysetMixin, TimestampMixin):
    __tablename__ = 'user_oauth_services'
    __table_args__ = (db.UniqueConstraint('user_id', 'service', name='_user_service_uc'),)

    user_id = db.Column(db.Integer, db.ForeignKey('users.pk'), nullable=False)
    service = db.Column(db.String(150), nullable=False)
    access_token = db.Column(db.Text, index=True)
    refresh_token = db.Column(db.Text)
    token_type = db.Column(db.String(150))
    access_token_expires = db.Column(db.DateTime(timezone=True))
    refresh_token_expires = db.Column(db.DateTime(timezone=True))


class OauthServices(QuerysetMixin):
    __tablename__ = 'oauth_services'

    service = db.Column(db.String(150), nullable=False)
    host = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(30))
    client_id = db.Column(db.String(255), nullable=False)
    client_secret = db.Column(db.String(255), nullable=False)

    @classmethod
    def get_service(cls, service: str) -> 'OauthServices':
        instance = cls.query.filter_by(service=service).first()
        if not instance:
            raise ValidationError([f'Service "{service}" does not exist'], field_name='service')
        return instance
