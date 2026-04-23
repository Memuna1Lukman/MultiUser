from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,String,TIMESTAMP,text,ForeignKey



class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    email = Column(String,nullable=False,index=True,unique=True)
    password = Column(String,nullable=False,index=True)
    role = Column(String,nullable=False,index=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    assigned = relationship("Tasks",foreign_keys="[Tasks.assigned_to]",back_populates="assigner")
    created = relationship("Tasks", foreign_keys="[Tasks.created_by]",back_populates="creator")
    user_comment = relationship("Comments",foreign_keys="[Comments.user_id]",back_populates="user")

class Tasks(Base):
    __tablename__ = "tasks"


    id = Column(Integer,primary_key=True)
    title = Column(String,nullable=False,index=True)
    created_by = Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
    creator = relationship("Users",
                           foreign_keys=[created_by],
                           back_populates="created")
    assigned_to = Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
    assigner = relationship("Users",
                            foreign_keys=[assigned_to],back_populates="assigned")
    status =   Column(String,nullable=False,index=True)   
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    deleted_at = Column(TIMESTAMP(timezone=True),nullable=True)
    task_comments = relationship("Comments",foreign_keys="[Comments.task_id]",back_populates="task")



class Comments(Base):

    __tablename__= "comments"
    id = Column(Integer,primary_key=True)
    content =  Column(String,nullable=False,index=True)
    task_id = Column(Integer,ForeignKey("tasks.id",ondelete='CASCADE'),nullable=False)
    task = relationship("Tasks",foreign_keys=[task_id],back_populates="task_comments")
    user_id = Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
    user = relationship("Users",foreign_keys=[user_id],back_populates="user_comment")
    created_at =  Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))