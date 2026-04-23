from jose import JWTError,jwt
from sqlalchemy.orm import Session
from . import models,schemas
from .database import get_db
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from datetime import datetime,timedelta
from fastapi import Depends,HTTPException,status


SECRET_KEY = settings.secret_key

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

ALGORITHM = settings.algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_token(id:int,role:str):
    data = {
        "id" : str(id),
        "role" : role
    }
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    jwt_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_token

def verify_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str = payload.get("id")
        role:str = payload.get("role")
        if id == None:
            raise credential_exception
        if role == None:
            raise credential_exception
        tokens = schemas.TokenData(id=id,role=role)
    except JWTError as e:
        print(e)
        raise credential_exception
    return tokens

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token=verify_token(token,credential_exception)
    user = db.query(models.Users).filter(
        models.Users.id==token.id,
        models.Users.role == token.role
    ).first()
    return user