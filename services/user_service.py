import logging
from datetime import datetime, UTC
from typing import Sequence, Optional

from db.dao.user_dao import UserDAO
from db.models import User


class UserService:
    def __init__(self, user_dao: UserDAO) -> None:
        self.user_dao = user_dao

    async def create_user(
            self,
            tg_id: int,
            first_name: str,
            last_name: str | None = None,
            username: str | None = None,
    ) -> User:
        new_user = User(
            id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        inserted = await self.user_dao.create_new(new_user)

        logging.info(f'Created User: id={new_user.id}')
        return inserted

    async def get_user_by_id(self, tg_id: int) -> User:
        user = await self.user_dao.get_by_id(tg_id)

        return user

    async def get_all_users(self) -> Sequence[User]:
        users = await self.user_dao.get_all_users()

        return users

    async def change_user_last_msg(self, tg_id: int) -> None:
        user = await self.get_user_by_id(tg_id)
        if not user:
            logging.warning(f'Unable to Update User: User not found (id={tg_id})')
            raise ValueError(f'User Not Found: id={tg_id}')

        date = datetime.now(UTC)
        data_to_update = {
            'last_message': date
        }

        await self.user_dao.update_user(tg_id, data_to_update)
        logging.info(f'Updated User: id={tg_id}')
