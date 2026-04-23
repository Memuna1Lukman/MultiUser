from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional



class CreateUser(BaseModel):
    id: Optional[int] = None
    email: str
    password: str
    role : str
    created_at: Optional[datetime] = None


class PostUser(BaseModel):
    id: Optional[int] = None
    email: str
    role : str
    created_at: Optional[datetime] = None
    model_config = {"from_attributes": True}


class TokenData(BaseModel):
    id: Optional[int] 
    role: Optional[str]


class AssignTasks(BaseModel):
    id:Optional[int] = None
    title: str
    
    created_by: Optional[int] = None
    assigned_to:int
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
class GetAdminTask(BaseModel):
    id:Optional[int] = None
    title: str
    created_by: Optional[int] = None
    assigned_to:int
    status: str  
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    model_config = {"from_attributes": True}

class UpdateTask(BaseModel):
    id:Optional[int] = None
    title: str
    created_by: Optional[int] = None
    assigned_to:int
    status: str  
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}
class GetAll(BaseModel):
    id:Optional[int] = None
    title: str
    created_by: Optional[int] = None
    assigned_to:int
    status: str  
    created_at: Optional[datetime] = None
    model_config = {"from_attributes": True}
class PostComment(BaseModel):
    id : Optional[int] = None
    content : str
    task_id : int
    user_id:Optional[int] = None
    created_at : Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CreateComment(BaseModel):
    id : Optional[int] = None
    content : str
    task_id : int
    user_id:Optional[int] = None
    created_at : Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}

class GetCommentIdde(CreateComment):
    pass
    model_config = {"from_attributes": True}    