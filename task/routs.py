from fastapi import APIRouter, Path, Depends, HTTPException, status, Query
from core.database import get_db
from sqlalchemy.orm import Session
from task.schema import * 
from task.models import Task_model
from users.models import User_model
from typing import  Optional
from fastapi.responses import JSONResponse
from auth.jwt import get_authenticated_user, get_authenticated_admin


router = APIRouter(tags=['tasks'])


# -- get all list tasks fpr specific user
@router.get('/tasks', response_model=list[TaskResponseSchema])
def retrieve_task_list(db:Session=Depends(get_db), 
                       completed:bool=Query(None, description='filter task that done or yet'),
                       limit:int=Query(10, gt=0, le=50, description='number retriever tasks'),
                       offset:int=Query(0, ge=0, description='number of next batch retriever tasks'),
                       user:User_model=Depends(get_authenticated_user)) :
    
    query = db.query(Task_model).filter_by(user_id=user.id)
    if completed is not None : 
        query = query.filter_by(is_completed=completed)
    
    result = query.limit(limit).offset(offset).all()
    return result


# -- get specific task for specific user
@router.get('/tasks/{task_id}', response_model=TaskResponseSchema)
def retrieve_task_detail(task_id:int=Path(..., gt=0), 
                         db:Session=Depends(get_db),
                         user:User_model=Depends(get_authenticated_user)) :
    
    try:
        task_obj = db.query(Task_model).filter_by(id=task_id, user_id=user.id).first()
    except:
        raise HTTPException(status_code=404, detail='task not found')
    return task_obj 


# -- insert data --
@router.post('/tasks', response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
def create_task(request:TaskCreateSchema, 
                db:Session=Depends(get_db), 
                user:User_model=Depends(get_authenticated_user)) :
    try:
        task_obj = Task_model(**request.model_dump(), user_id=user.id)
        db.add(task_obj)
        db.commit()
        db.refresh(task_obj)
        print(f'type: {task_obj} -- parts:{task_obj.__dict__}')
        return task_obj
    
    except Exception as e:
        db.rollback() 
        print(f"Error creating task: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


@router.put('/tasks/{task_id}', response_model=TaskResponseSchema)
def update_task(request:TaskUpdateSchema, task_id:int=Path(..., gt=0), 
                db:Session=Depends(get_db),
                user:User_model=Depends(get_authenticated_user)) :
    
    task_obj = db.query(Task_model).filter_by(user_id=user.id, id=task_id).first()
    if not task_obj : 
        raise HTTPException(status_code=404, detail=f'task id:{task_id} not found')
    try:
        #convert pydantic class to dict
        #exclude_unset param: process fields that user send it, not more >> faster
        update_data = request.model_dump(exclude_unset=True)
        for field,value in update_data.items() :
            print(f'field:{field} -- value:{value}')
            setattr(task_obj, field, value)
        db.commit()
        db.refresh(task_obj)
        return task_obj
    
    except Exception as e:
        db.rollback() 
        print(f"Error edit task: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='server error')        


@router.delete('/tasks/{task_id}', status_code=status.HTTP_200_OK )
def delete_task(task_id:int=Path(..., gt=0), 
                db:Session=Depends(get_db),
                user:User_model=Depends(get_authenticated_admin)) :
    '''
    status_code (204) : dont habe BODY. so 1-dont have return or BODY. 2- 0 bytes.its good when have milion requests
    '''
    
    task_obj = db.query(Task_model).filter_by(user_id=user.id, id=task_id).first()
    if not task_obj : 
        raise HTTPException(status_code=404, detail=f'task id:{task_id} not found')
    
    try:
        db.delete(task_obj)
        db.commit()
        return JSONResponse(
            content={"message": f"{task_id} delete succesfully"},
            status_code=status.HTTP_200_OK )
        
    except Exception as e:
        db.rollback()
        print(f"Error deleting task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='internal error in delete')
    
