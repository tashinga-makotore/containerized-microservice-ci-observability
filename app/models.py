from pydantic import BaseModel


class TaskCreate(BaseModel):
    name: str
    status: str = "pending"
    
