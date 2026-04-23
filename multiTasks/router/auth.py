from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,utils,models,oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/login",
    tags=['Login']
)

@router.post("/")
def login_user(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    username = db.query(models.Users).filter(
        models.Users.email == user.username
    ).first()
    if not username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,details=f"Invaliid credentails")
    print(f"DEBUG: Plain: {user.password}")
    print(f"DEBUG: Hashed from DB: {username.password}")
    password_confirrm= utils.unhash_password(user.password,username.password)
    if not password_confirrm:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,details=f"Invaliid credentails")
    access_token = oauth.create_token(id=username.id,role=username.role)
    print(access_token)
    return{"token": access_token,"token_type":"bearer"}