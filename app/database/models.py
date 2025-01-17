from sqlalchemy import Column, DateTime, BigInteger, func

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
