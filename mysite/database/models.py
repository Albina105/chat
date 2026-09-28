from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String(100))
    owner: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    group_people: Mapped[List['GroupPeople']] = relationship(
        back_populates='people_group', cascade='all, delete-orphan')
    group_messages: Mapped[List['GroupMessage']] = relationship(
        back_populates='message_group', cascade='all, delete-orphan')


class GroupPeople(Base):
    __tablename__ = 'group_people'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id', ondelete='CASCADE'))
    user: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    people_group: Mapped['Group'] = relationship(Group, back_populates='group_people')





class GroupMessage(Base):
    __tablename__ = 'group_messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id', ondelete='CASCADE'))
    user: Mapped[int] = mapped_column(Integer)
    message: Mapped[str] = mapped_column(Text, nullable=True)
    file_path: Mapped[str] = mapped_column(String(255), nullable=True)
    file_type: Mapped[str] = mapped_column(String(50), nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    message_group: Mapped['Group'] = relationship(Group, back_populates='group_messages')


# models