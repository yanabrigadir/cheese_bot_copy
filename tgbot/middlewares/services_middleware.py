from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update

from services.user_service import UserService
from db.dao.user_dao import UserDAO
from sqlalchemy.ext.asyncio import AsyncSession


class ServicesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        session: AsyncSession = data["session"]
        user_dao = UserDAO(session)
        user_service = UserService(user_dao)
        data["user_service"] = user_service

        return await handler(event, data)
