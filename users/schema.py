from pydantic import BaseModel , Field, ConfigDict, field_validator, model_validator, validate_email
from typing import Optional
from datetime import datetime
import  re


class UserBase(BaseModel) :
    username :str = Field(..., max_length=64, description='user name and family')
    #email:str = Field(..., max_length=64, description='valid email or gmail')
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('username')
    @classmethod
    def name_normilze(cls, name:str) :
        return name.lower()

    
# --- Login ---    
class UserLoginSchema(UserBase) :
    password:str = Field(..., min_length=3, max_length=128, description='must contain at least 1 capital letter & special sign & a number')
    
    @field_validator('password')
    @classmethod
    def check_password(cls, val: str) -> str:
        if not re.search(r'\d', val):
            raise ValueError('password must have at least 1 number')

        if not re.search(r'[A-Z]', val):
            raise ValueError('password must have at least 1 capital charcter')

        if not re.search(r'[!@#$%^&(),.?":{}|<>]', val):
            raise ValueError('password must have at least 1 special charcter')

        return val
     

class UserLoginResponseSchema(UserBase) :
    id:int = Field(..., description='this is a unique')


# -- Register -- 
class UserRegisterCreateSchema(UserLoginSchema) :
    '''
    mode='after' . first pydantic check the field then pass to the model_validator
    '''
    password_confirm :str = Field(...,  min_length=3, max_length=128, description='Repeat your password') 
    
    @model_validator(mode='after')
    def check_password_match(self):
        pw1 = self.password
        pw2 = self.password_confirm
        if pw1 != pw2 :
            raise ValueError('the passwords are not same')
        return self
    
class UserRegisterResponseSchema(UserBase) :
    id:int = Field(..., description='this is a unique')
    is_active:bool = Field(True, description='active member or offline for long time')
    created_date:datetime = Field(..., description='the time user define or create task')
    updated_date:datetime = Field(..., description='the time user update the task')    


# -- Refresh token --   
class UserRefreshTokenSchema(BaseModel):
    token:str = Field(..., description='refresh token of the user')