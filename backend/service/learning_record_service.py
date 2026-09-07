from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from model.learning_record import LearningRecord
from schema.learning_record import LearningRecordCreate

async def create_record(
        db:AsyncSession,
        record_data:LearningRecordCreate,
        user_id:int
):
    # 查询
    # 创建记录对象
    new_record = LearningRecord(
        user_id = user_id,
        title=record_data.title,
        content=record_data.content,
        study_time=record_data.study_time
    )
    db.add(new_record)

    # 先把当前修改发送给数据库执行，但暂时不正式结束整个事务
    await db.flush()

    await db.refresh(new_record)
    return new_record

async def get_records_by_user(
        db:AsyncSession,
        user_id:int
) :
    result = await db.execute(
        select(LearningRecord).where(LearningRecord.user_id == user_id)
    )
    record=  result.scalars().all()
    return record
