import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class AnnouncementImages(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "announcement_images"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    path = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    announcement_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("announcements.id"))
    announcement = orm.relationship("Announcements", back_populates="images")
