from datetime import datetime
from typing import Literal
from pydantic import BaseModel,ConfigDict

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )


class ChatMessageResponse(BaseModel):
    id: int
    conversation_id: str
    role: Literal[
        "user",
        "assistant"
    ]
    content: str
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )