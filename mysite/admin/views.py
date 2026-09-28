from sqladmin import ModelView

from mysite.database.models import Group, GroupPeople, GroupMessage


class GroupAdmin(ModelView, model=Group):
    column_list = [Group.id, Group.group_name, Group.owner, Group.created_date]


class GroupPeopleAdmin(ModelView, model=GroupPeople):
    column_list = [GroupPeople.id, GroupPeople.group_id, GroupPeople.user, GroupPeople.created_date]


class GroupMessageAdmin(ModelView, model=GroupMessage):
    column_list = [
        GroupMessage.id,
        GroupMessage.group_id,
        GroupMessage.user,
        GroupMessage.message,
        GroupMessage.created_date,
    ]