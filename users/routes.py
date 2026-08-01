from fastapi import APIRouter, Path, Depends, HTTPException, status, Query
from core.database import get_db
from sqlalchemy.orm import Session
from users.schema import * 
from users.models import User_model, Token_model, User_type
from typing import  Optional
from fastapi.responses import JSONResponse
from auth.jwt import generate_access_token, generate_refresh_token, get_authenticated_user, decode_refresh_token, get_authenticated_admin
import jwt
from core.config import settings



router = APIRouter(tags=['users'], prefix='/users')


# -- register -- 
@router.post('/register')
def user_register(request:UserRegisterCreateSchema, db:Session=Depends(get_db)) :
    #check username exist
    if db.query(User_model).filter_by(username=request.username).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='the user exist in database')
    user_obj = User_model(username=request.username)
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return JSONResponse(content={'message': 'User registered successfully'}) 
    

# -- login --    
@router.post('/login')
def user_login(request:UserLoginSchema, db:Session=Depends(get_db)) :
    user_obj = db.query(User_model).filter_by(username=request.username).first()
    if not user_obj :
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password')
    if not user_obj.verify_password(request.password) :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password')
    
    access_token = generate_access_token(user_id=user_obj.id)
    refresh_token = generate_refresh_token(user_id=user_obj.id)
    
    new_token = Token_model(user_id=user_obj.id, token=refresh_token)    
    db.add(new_token)    
    db.commit()    
    db.refresh(new_token)
    return JSONResponse(content={'message': 'Login successful', 'access_token': access_token, 'refresh_token':refresh_token, 'token_type': "bearer"})    


# -- refresh token --
@router.post('/refresh_token')
def user_refresh_token(request:UserRefreshTokenSchema, db: Session = Depends(get_db)):
    # refresh_token -> access_token
    user_id = decode_refresh_token(request.token)
    access_token = generate_access_token(user_id=user_id)
    return JSONResponse(content={"access_token" : access_token} )


# -- change authrization ( user -> admin ) -- 
@router.patch('/make-admin')
def make_admin(user_id:int, db:Session = Depends(get_db), admin:User_model = Depends(get_authenticated_admin)  ):
    
    user = db.query(User_model).filter(User_model.id == user_id).first()
    user.user_type = User_type.ADMIN
    db.commit()
    return {"message": f"User {user.username} is now an admin!"}