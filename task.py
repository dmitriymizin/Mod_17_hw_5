from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from Module_17.HW_mod_17.hw_17_4.app.backend.db_depends import get_db
from typing import Annotated
from Module_17.HW_mod_17.hw_17_4.app.models import Task
from Module_17.HW_mod_17.hw_17_4.app.models import User
from Module_17.HW_mod_17.hw_17_4.app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_task(db: Annotated[Session, Depends(get_db)]):
    list_of_task = db.scalars(select(Task)).all()
    return list_of_task

@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    single_task = db.scalar(select(Task).where(Task.id == task_id))
    if single_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    return single_task

@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    single_user = db.scalar(select(User).where(User.id == user_id))
    if single_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    task_slug = slugify(create_task.title)
    new_task = Task(title=create_task.title,
                    content=create_task.content,
                    priority=create_task.priority,
                    user_id=single_user.id,
                    slug=task_slug
                    )
    db.add(new_task)
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask):
    single_task = db.scalar(select(Task).where(Task.id == task_id))
    if single_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(update(Task).where(Task.id == task_id).values(
        title=create_task.title,
        content=create_task.content,
        priority=create_task.priority
    ))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful'
    }

@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    single_task = db.scalar(select(Task).where(Task.id == task_id))
    if single_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task delete is successful'
    }