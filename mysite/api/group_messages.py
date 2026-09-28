from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from mysite.database.models import Group, GroupPeople, GroupMessage
from mysite.database.schema import (
    GroupMessageCreateSchema,
    GroupMessageUpdateSchema,
    GroupMessageOutputSchema,
)
from mysite.database.db import SessionLocal
from .dependencies import get_current_user

group_message_router = APIRouter(prefix='/group-messages', tags=['Group Messages'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@group_message_router.post(path='/', response_model=GroupMessageOutputSchema)
async def group_message_create(message: GroupMessageCreateSchema, current_user: Annotated[dict, Depends(get_current_user)],
                      db: Session = Depends(get_db)):
    group_db = db.query(Group).filter(Group.id == message.group_id).first()

    if not group_db:
        raise HTTPException(detail='Мындай группа жок', status_code=404)

    group_people_db = db.query(GroupPeople).filter(
        GroupPeople.group_id == message.group_id,
        GroupPeople.user == current_user['id']
    ).first()

    if not group_people_db:
        raise HTTPException(detail='Колдонуучу бул группада жок', status_code=400)

    message_db = GroupMessage(
        group_id=message.group_id,
        user=current_user['id'],
        message=message.message,
    )

    db.add(message_db)
    db.commit()
    db.refresh(message_db)

    return message_db


@group_message_router.get('/group/{group_id}/', response_model=List[GroupMessageOutputSchema])
async def group_message_list(
    group_id: int,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    member = db.query(GroupPeople).filter(
        GroupPeople.group_id == group_id,
        GroupPeople.user == current_user['id']
    ).first()

    if not member:
        raise HTTPException(detail='Сиз бул группада жоксуз', status_code=404)

    all_messages = db.query(GroupMessage).filter(
        GroupMessage.group_id == group_id
    ).order_by(GroupMessage.created_date.asc()).all()

    return all_messages



@group_message_router.get('/{message_id}/', response_model=GroupMessageOutputSchema)
async def group_message_detail(
    message_id: int,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    message_db = db.query(GroupMessage).filter(GroupMessage.id == message_id).first()

    if not message_db:
        raise HTTPException(detail='Мындай билдирүү жок', status_code=404)

    return message_db


@group_message_router.put('/{message_id}/', response_model=dict)
async def group_message_update(
    message_id: int,
    message: GroupMessageUpdateSchema,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    message_db = db.query(GroupMessage).filter(GroupMessage.id == message_id).first()

    if not message_db:
        raise HTTPException(detail='Мындай билдирүү жок', status_code=404)

    if message_db.user != current_user['id']:
        raise HTTPException(detail='Маалыматты озгортууго болбойт', status_code=403)

    message_db.message = message.message

    db.commit()
    db.refresh(message_db)

    return {'message': 'Билдирүү өзгөртүлдү'}


@group_message_router.delete('/{message_id}/', response_model=dict)
async def group_message_delete(
    message_id: int,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    message_db = db.query(GroupMessage).filter(GroupMessage.id == message_id).first()

    if not message_db:
        raise HTTPException(detail='Мындай билдирүү жок', status_code=404)

    if message_db.user != current_user['id']:
        raise HTTPException(detail='Маалыматты озгортууго болбойт', status_code=403)

    db.delete(message_db)
    db.commit()

    return {'message': 'Билдирүү өчүрүлдү'}