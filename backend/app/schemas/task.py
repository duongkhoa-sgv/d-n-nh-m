from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"   
    status: Optional[str] = "todo"        
    deadline: Optional[datetime] = None


class TaskCreate(TaskBase):
    project_id: int
    sprint_id: Optional[int] = None
    assignee_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[str]
    status: Optional[str]
    deadline: Optional[datetime]
    assignee_id: Optional[int]


class TaskResponse(TaskBase):
    id: int
    project_id: int
    sprint_id: Optional[int]
    assignee_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
