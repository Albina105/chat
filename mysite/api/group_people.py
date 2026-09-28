from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from mysite.database.models import Group, GroupPeople
from mysite.database.schema import GroupPeopleCreateSchema, GroupPeopleOutputSchema
from mysite.database.db import SessionLocal
from .dependencies import get_current_user

group_people_router = APIRouter(prefix='/group-people', tags=['Group People'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@group_people_router.post('/', response_model=GroupPeopleOutputSchema)
async def group_people_create(
        group_people: GroupPeopleCreateSchema,
        current_user: Annotated[dict, Depends(get_current_user)],
        db: Session = Depends(get_db)
):
    group_db = db.query(Group).filter(Group.id == group_people.group_id).first()

    if not group_db:
        raise HTTPException(detail='Мындай группа жок', status_code=404)
    if group_db.owner != current_user['id']:
        raise HTTPException(status_code=403, detail='Группага адамды группанын ээси гана кошо алат')

    existing_user = db.query(GroupPeople).filter(
        GroupPeople.group_id == group_people.group_id,
        GroupPeople.user == group_people.user
    ).first()

    if existing_user:
        raise HTTPException(detail='Бул колдонуучу группада мурунтан эле бар', status_code=400)

    group_people_db = GroupPeople(group_id=group_people.group_id, user=group_people.user)

    db.add(group_people_db)
    db.commit()
    db.refresh(group_people_db)

    return group_people_db


@group_people_router.get('/', response_model=List[GroupPeopleOutputSchema])
async def group_people_list(db: Session = Depends(get_db)):
    return db.query(GroupPeople).all()


@group_people_router.get('/{group_people_id}/', response_model=GroupPeopleOutputSchema)
async def group_people_detail(group_people_id: int, db: Session = Depends(get_db)):
    group_people_db = db.query(GroupPeople).filter(GroupPeople.id == group_people_id).first()

    if not group_people_db:
        raise HTTPException(detail='Мындай группа мүчөсү жок', status_code=404)

    return group_people_db


@group_people_router.delete('/{group_people_id}/', response_model=dict)
async def group_people_delete(group_people_id: int, db: Session = Depends(get_db)):
    group_people_db = db.query(GroupPeople).filter(GroupPeople.id == group_people_id).first()

    if not group_people_db:
        raise HTTPException(detail='Мындай группа мүчөсү жок', status_code=404)

    db.delete(group_people_db)
    db.commit()

    return {'message': 'Колдонуучу группадан өчүрүлдү'}