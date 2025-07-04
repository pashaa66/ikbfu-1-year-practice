import datetime as dt
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    phone_number = sqlalchemy.Column(sqlalchemy.
                                     String, unique=True, nullable=True)
    experience = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    deals = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    role = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    profile_picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    announcement = orm.relationship('Announcements', back_populates='user')
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=dt.datetime.date(dt.
                                                              datetime.now()))

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
