import uuid
from app.core.database import Base
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID


class Shop(Base):
    __tablename__ = "shops"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    description = Column(String(300), nullable=False)
    location = Column(String(100), nullable=False)
    email = Column(String(200),nullable=False)
    phone = Column(String(15), nullable=False)
    owner_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)