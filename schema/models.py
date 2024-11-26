from sqlalchemy import Column, String, DateTime, func, Integer
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from db import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(SQL_UUID(as_uuid=True), nullable=False, index=True)
    user_question = Column(String, nullable=False)
    bot_answer = Column(String, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
