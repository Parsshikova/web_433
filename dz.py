from db import Base


class UserMessage(Base):

    pass
    id= 
    ssesion_id
    message = 
class UserSession(Base):
    pass
------------------------------------------------

from fastapi import APIRouter
router = APIRouter(
    prefix="chat",
    tags=["chat"],
)
@router.post("/session")
async new_session():
    pass
@router.get("/session")
async session():
    pass
@router.post("/message")
async message():
    pass
@router.get("/message")
async message():
    pass
--------------------------------------------------------------------------------------------
from pydantic import BaseModel, Field

class NewSession(BaseModel):
    pass
class SessionResponce(BaseModel):
    pass
class NewMessage(BaseModel):
    pass
class MessageResponce(BaseModel):
    pass
