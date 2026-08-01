from sqlalchemy import Column, String, Integer, func, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from core.database import Base
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from enum import Enum


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto", bcrypt__rounds=12)


class User_type(Enum):
    ADMIN = 'admin'
    USER = 'user'
    
    
class User_model(Base) :
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(128), nullable=False) 
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    user_type = Column(SQLEnum(User_type), nullable=False, default=User_type.USER)
    
    #relation(1user-many tasks)
    tasks = relationship('Task_model', back_populates='user', cascade="all, delete-orphan")    
    
    def set_password(self, plain_password: str) -> None:
        MAX_LEN  = 72
        self.password = pwd_context.hash(plain_password[:MAX_LEN])
    
    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)  
    
    #relation with token 
    token = relationship('Token_model', back_populates='user', uselist=False) 
    
    
    
class Token_model(Base)  :
    __tablename__ = 'tokens'
    
    id =  Column(Integer, primary_key=True, autoincrement=True)
    user_id =  Column(Integer, ForeignKey('users.id')) 
    
    token = Column(String, nullable=False)
    created_date = Column(DateTime, server_default=func.now())
    
    ##relation with user 
    user = relationship('User_model', back_populates='token')