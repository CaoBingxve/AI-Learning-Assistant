from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class LearningRecordCreate(BaseModel):
    title: str=Field(min_length=1,max_length=255)
    content: str
    study_time: int=Field(gt=0)

class LearningRecordResponse(BaseModel):
    id:int
    user_id:int
    title:str
    content:str
    study_time:int
    created_at:datetime
    class Config:
        from_attributes = True