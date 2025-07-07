import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Announcements(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'announcements'

    id = sqlalchemy.Column(sqlalchemy.
                           Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    announcement_type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    square = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    visits = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    kitchen_square = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    number_of_rooms = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    is_sell = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    floor = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    number_of_floors = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    year_of_construction = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    main_image = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.
                                ForeignKey('users.id'), nullable=True)
    user = orm.relationship('User')

    images = orm.relationship("AnnouncementImage",
                              back_populates="announcement",
                              cascade="all, delete", lazy="joined")
