import logging
from typing import Sequence, Optional
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from db.models import User


class UserDAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_new(self, user: User) -> User:
        stmt = insert(User).values(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        ).returning(User)

        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            inserted = result.scalar()
        except IntegrityError:
            logging.warning(f"Failed to create User: already exists "
                           f"(id={user.id})")
            await self.session.rollback()
            raise UserAlreadyExistsError(user.id)

        return inserted

    async def get_by_id(self, tg_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == tg_id)

        result = await self.session.execute(stmt)
        data = result.scalar()

        return data

    async def get_all_users(self) -> Sequence[User]:
        stmt = select(User)

        result = await self.session.execute(stmt)
        data = result.scalars().all()

        return data

    async def update_user(self, tg_id: int, data: dict) -> Optional[User]:
        stmt = update(User).where(User.id == tg_id).values(
            **data
        ).returning(User)

        result = await self.session.execute(stmt)
        await self.session.commit()
        data = result.scalar()

        return data


class UserAlreadyExistsError(Exception):
    """Raised when trying to create a User that already exists."""

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        message = f"User already exists: id={self.user_id}"
        super().__init__(message)
