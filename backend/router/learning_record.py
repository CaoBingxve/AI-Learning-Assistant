from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schema.learning_record import (
    LearningRecordResponse,
    LearningRecordCreate
)
from config.database import get_database
from model.user import User

from service.learning_record_service import (
    create_record,
    get_records_by_user
)
from utils.auth import get_current_user

router = APIRouter(prefix="/records",tags=["学习记录模块"])

@router.post(
    "",
    response_model=LearningRecordResponse
)
async def create_learning_record(
    record: LearningRecordCreate,
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    new_record = await create_record(db,record,current_user.id)
    return new_record

@router.get(
    "",
    response_model=list[LearningRecordResponse]
)
async def get_learning_records(
    db: AsyncSession = Depends(get_database),
    current_user: User = Depends(get_current_user)
):
    records = await get_records_by_user(db,current_user.id )
    return records