from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import models,oauth,schemas
from ..database import get_db
from typing import List
from datetime import datetime
from typing import Optional
router=APIRouter(
    prefix="/admin",
    tags=['Assign']
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.GetAdminTask)
def assign_tasks(admin:schemas.AssignTasks,
    db:Session=Depends(get_db),
    get_current_user=Depends(oauth.get_current_user)):
    # i need to know if the person is a logged in user
    query_user = db.query(models.Users).filter(
        models.Users.id == get_current_user.id,
        models.Users.role == get_current_user.role
    ).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    # only admins are allowed to assign tasks
    
    if get_current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed to assign tasks") 
   
    
    tasks = admin.dict()
    tasks['created_by'] = get_current_user.id
    
    tasks = models.Tasks(**tasks)
    db.add(tasks)
    db.commit()
    db.refresh(tasks)
    return tasks

@router.get("/",response_model=List[schemas.GetAdminTask])
def get_tasks(db:Session=Depends(get_db),
              get_current_user=Depends(oauth.get_current_user),limit:int=10,offset:int=0):
    query_user = db.query(models.Users).filter(
        models.Users.id == get_current_user.id,
        models.Users.role == get_current_user.role
    ).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    if get_current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed to assign tasks")
    query_tasks = db.query(models.Tasks).filter(
        models.Tasks.created_by == get_current_user.id
    )
    count = query_tasks.count()
    query_limit = query_tasks.offset(offset).limit(limit).all()
    if not query_limit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Tasks are not found") 
    return {"query": query_limit,"count": count}


@router.put("/{id}",response_model=schemas.UpdateTask)
def update_task(id:str,admin:schemas.AssignTasks,
    db:Session=Depends(get_db),
    get_current_user=Depends(oauth.get_current_user)):
    query_user = db.query(models.Users).filter(
        models.Users.id == get_current_user.id,
        models.Users.role == get_current_user.role
    ).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    # only admins are allowed to assign tasks
    
    if get_current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed to assign tasks") 

    query_table = db.query(models.Tasks).filter(
        models.Tasks.id==id
    )
    query_update = query_table.first()
    if not query_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    updated_data =admin.dict(exclude_unset=True)
    updated_data['updated_at'] = datetime.utcnow()
    query_table.update(updated_data,synchronize_session=False)
    db.commit()
    return query_update


@router.delete("/{id}",response_model=schemas.GetAdminTask)
def soft_delete(id:str,
                admin:schemas.AssignTasks,
    db:Session=Depends(get_db),
    get_current_user=Depends(oauth.get_current_user)):
    query_user = db.query(models.Users).filter(
        models.Users.id == get_current_user.id,
        models.Users.role == get_current_user.role
    ).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    # only admins are allowed to assign tasks
    
    if get_current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed to assign tasks") 
    query_table = db.query(models.Tasks).filter(
        models.Tasks.id == id
    )
    deleted = query_table.first()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    deleted_data = admin.dict()
    deleted_data['deleted_at'] = datetime.utcnow()
    db.commit(deleted)
    return deleted

# This is a query that are users can get access to that i both admin and also memebers


@router.get("/all",response_model=List[schemas.GetAll])
def paginations(db:Session=Depends(get_db),get_current_user=Depends(oauth.get_current_user),limit:int=10,offset:int=0,status:Optional[str]=None):
    query_user = db.query(models.Users).filter(
        models.Users.id == get_current_user.id,
        models.Users.role == get_current_user.role
    ).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    
    if status:
        query_tasks = db.query(models.Tasks).filter(models.Tasks.status == status)
    query_tasks = db.query(models.Tasks).filter(
        models.Tasks.assigned_to == get_current_user.id
    )
    query_limit = query_tasks.offset(offset).limit(limit).all()

    if not query_limit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"task is not found")
    return query_limit




