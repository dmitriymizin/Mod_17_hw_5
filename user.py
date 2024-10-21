from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from Module_17.HW_mod_17.hw_17_4.app.backend.db_depends import get_db
from typing import Annotated
from Module_17.HW_mod_17.hw_17_4.app.models import User
from Module_17.HW_mod_17.hw_17_4.app.models import Task
from Module_17.HW_mod_17.hw_17_4.app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    list_of_users = db.scalars(select(User)).all()
    return list_of_users

@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    single_user = db.scalar(select(User).where(User.id == user_id))
    if single_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    return single_user


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                    firstname=create_user.firstname,
                                    lastname=create_user.lastname,
                                    age=create_user.age,
                                    slug=slugify(create_user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    single_user = db.scalar(select(User).where(User.id == user_id))
    if single_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(update(User).where(User.id == user_id).values(
        firstname=update_user.firstname,
        lastname=update_user.lastname,
        age=update_user.age
        ))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful'
    }

@router.get("/{user_id}/tasks")
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    single_user = db.scalar(select(User).where(User.id == user_id))
    if single_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    user_tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    return user_tasks

@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    single_user = db.scalar(select(User).where(User.id == user_id))
    if single_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful'
    }