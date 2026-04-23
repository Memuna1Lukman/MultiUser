from fastapi import APIRouter,Depends,HTTPException,status
from ..database import get_db
from .. import models,schemas,utils
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/signup",
    tags=['Signup']
)



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostUser)
def sign_user_up(user:schemas.CreateUser,db:Session = Depends(get_db)):
    hash_password = utils.hash_password(user.password)
    new_user = user.dict()
    new_user['password'] = hash_password
    new_user = models.Users(**new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user





