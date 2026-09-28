from fastapi import FastAPI
import uvicorn

from mysite.api import groups, group_people, group_messages, websocket_chat
from mysite.admin.setup import setup_admin

group_app = FastAPI(title='Group Chat Service')
group_app.include_router(groups.group_router)
group_app.include_router(group_people.group_people_router)
group_app.include_router(group_messages.group_message_router)
group_app.include_router(websocket_chat.websocket_router)
setup_admin(group_app)


if __name__ == '__main__':
    uvicorn.run(group_app, host='127.0.0.1', port=8004)

