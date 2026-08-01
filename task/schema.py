from pydantic import BaseModel , Field, ConfigDict
from typing import Optional
from datetime import datetime


class TaskBaseSchema(BaseModel) :
    title :str = Field(..., max_length=128, description='task title')
    description: Optional[str] = Field(None, max_length=512, description='a brief summary about what should to do ')
    is_completed: bool = Field(..., description='task status')

class TaskCreateSchema(TaskBaseSchema) :
    pass

class TaskUpdateSchema(TaskBaseSchema) :
    title: str | None = Field(None, max_length=128)
    description: str | None = Field(None, max_length=512)
    is_completed: bool | None = Field(None)


class TaskResponseSchema(TaskBaseSchema) :
    """
    model_config :must read data from database , convert to pydantic model. so let pydantic
                  to use SQLAlchemy classes.
    """
    
    id: int = Field(..., description='this is a unique')
    created_date: datetime = Field(..., description='the time user define or create task')
    updated_date: datetime = Field(..., description='the time user update the task')
    
    model_config = ConfigDict(from_attributes=True)
