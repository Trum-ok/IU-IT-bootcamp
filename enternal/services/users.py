from enternal.services.models.domains import User
from enternal.storages.sqlalchemy_db import db

async def get_user_info_by_id(user_id: str) -> User:
    return await db.get_user_by_id(user_id)


async def get_user_info_by_login(login: str) -> User:
    return await db.get_user_by_login(login)


async def get_users_unfo() -> list[User]:
    return await db.get_users()


async def create_user(user: User) -> None:
    await db.add_user(user)


async def delete_user(user_id: str) -> None:
    await db.remove_user(user_id)
