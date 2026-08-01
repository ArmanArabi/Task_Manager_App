from sqlalchemy import Column, String, Integer, text, func, Boolean, DateTime, ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship


class Task_model(Base) :
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    description = Column(String(512), nullable=True) 
    is_completed = Column(Boolean, default=False)
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    
    #relation(1user-many tasks)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User_model', back_populates='tasks')