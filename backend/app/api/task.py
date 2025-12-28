from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse
)
from app.services import task_service

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# Create task 
@router.post("/", response_model=TaskResponse)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db)
):
    return task_service.create_task(db, data)


# Get tasks by project 
@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    project_id: int,
    db: Session = Depends(get_db)
):
    return task_service.get_tasks(db, project_id)


# Get task detail 
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Update task 
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = task_service.update_task(db, task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Delete task 
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    success = task_service.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
