import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
    __tablename__ = 'departments'
    user = orm.relationship('User')
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    chief = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("users.id"))
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
