from sqlalchemy.orm import Session
from schema import ChatHistory
from typing import List
from db import SessionLocal
from uuid import UUID


def get_chat_history(session_id: UUID) -> List[ChatHistory]:
    """
    Fetch chat history for a given session_id.
    """
    with SessionLocal() as db:
        return (db
                .query(ChatHistory)
                .filter(ChatHistory.session_id == session_id)
                .order_by(ChatHistory.timestamp)
                .all()
                )


def save_chat_history(session_id: UUID, question: str, answer: str) -> None:
    """
    Save a new question-answer pair to the database.
    """
    with SessionLocal() as db:
        new_entry = ChatHistory(
            session_id=session_id,
            user_question=question,
            bot_answer=answer,
        )
        db.add(new_entry)
        db.commit()
