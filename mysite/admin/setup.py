from fastapi import FastAPI
from sqladmin import Admin

from mysite.database.db import engine
from .views import GroupAdmin, GroupPeopleAdmin, GroupMessageAdmin


def setup_admin(group_app: FastAPI):
    admin = Admin(group_app, engine)
    admin.add_view(GroupAdmin)
    admin.add_view(GroupPeopleAdmin)
    admin.add_view(GroupMessageAdmin)