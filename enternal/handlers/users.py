from fastapi import APIRouter
from services.domains import User
from services.users import (
    get_user_info_by_id,
    get_user_info_by_login,
    get_users_unfo,
    delete_user,
    add_user
)


user_router = APIRouter(tags=['Users'])

@user_router.get('/user')
async def handler_get_user_info(user: User):
    if user.id is not None:
        return await get_user_info_by_id(user.id)
    else:
        return await get_user_info_by_login(user.login)


@user_router.get('/users')
async def handler_get_users_info():
    return await get_users_unfo()


@user_router.post('/user/create')
async def handler_create_user(user: User):
    await add_user(user)


@user_router.delete('/user/delete')
async def handler_delete_user(user: User):
    await delete_user(user.id)
