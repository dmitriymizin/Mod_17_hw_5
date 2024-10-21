from Module_17.HW_mod_17.hw_17_4.app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from Module_17.HW_mod_17.hw_17_4.app.models.task_mod import Task

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)


    tasks = relationship('Task', back_populates='user')
