from fastapi import Depends,HTTPException,status,APIRouter
from .. import models,oauth,schemas
from ..database import get_db
from sqlalchemy.orm import Session
from datetime import datetime



router = APIRouter(
    prefix="/comment",
    tags=['Comments']
)


# post comment by validating  the user as a signin user
# validate the presence of the task_id
# thhen post or add to the comments table


# im sorry i just do not like writing comments



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.CreateComment)
def post_comment(comment:schemas.PostComment,db:Session=Depends(get_db),get_current_user=Depends(oauth.get_current_user)):
    query_user = db.query(models.Users).filter(
        models.Users.id == get_current_user.id
    ).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    query_task= db.query(models.Tasks).filter(models.Tasks.id == comment.task_id).first()
    if not query_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    comments=comment.dict()
    comments['user_id'] = get_current_user.id
    comments = models.Comments(**comments)
    db.add(comments)
    db.commit()
    db.refresh(comments)
    return comments


@router.get("/{id}",response_model=schemas.GetCommentIdde)
def get_comments(id:int,db:Session=Depends(get_db),get_current_user=Depends(oauth.get_current_user)):
    query_user = db.query(models.Users).filter(
        models.Users.id == get_current_user.id
    ).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    query_comment = db.query(models.Comments).filter(models.Comments.id==id).first()
    if not query_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    return query_comment


@router.put("/{id}",response_model=schemas.CreateComment)
def update_comment(id:int,comment:schemas.PostComment,db:Session=Depends(get_db),get_current_user=Depends(oauth.get_current_user)):
    query_user = db.query(models.Users).filter(
        models.Users.id == get_current_user.id
    ).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    query_task= db.query(models.Tasks).filter(models.Tasks.id == comment.task_id).first()
    if not query_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    query_comment = db.query(models.Comments).filter(models.Comments.id == id)
    query = query_comment.first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    comment_data = comment.dict(exclude_unset=True)
    comment_data['updated_at'] = datetime.utcnow()
    query.update(comment_data,synchronize_session=False)
    db.commit()
    return query



@router.delete("/{id}")
def delete_comment(id:int,db:Session=Depends(get_db),get_current_user=Depends(oauth.get_current_user)):
    query_user = db.query(models.Users).filter(
        models.Users.id == get_current_user.id
    ).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    query_comment = db.query(models.Comments).filter(models.Comments.id == id)
    query = query_comment.first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    db.delete(query)
    db.commit()
    return query

@router.get("/",response_model=schemas.GetCommentIdde)
def get_comment(db:Session=Depends(get_db),get_current_user=Depends(oauth.get_current_user),limit:int=10,offset:int=0):
    query_user = db.query(models.Users).filter(
        models.Users.id == get_current_user.id
    ).first()
    if not query_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{query_user} is not found")
    query_tasks = db.query(models.Tasks).filter(
        models.Comments.user_id == get_current_user.id
    )
    query_limit = query_tasks.offset(offset).limit(limit).all()
    if not query_limit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Tasks is not found")
    return query_limit

