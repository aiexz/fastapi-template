from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .models import User


class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_async_engine(db_url, pool_recycle=3600, echo=False)
        self.sessionmaker = async_sessionmaker(bind=self.engine)

    def __call__(self):
        return self

    async def ping(self) -> bool:
        """Check if the database is alive"""
        async with self.sessionmaker() as session:
            result = await session.execute(text("SELECT 1"))
            if result.scalars().first() == 1:
                return True
            else:
                return False

    async def get_user(self, user_id: int) -> User:
        """Get user by id"""
        async with self.sessionmaker() as session:
            asset = await session.execute(
                    select(User)
                    .where(User.id == user_id)
            )
            return asset.scalars().first()
