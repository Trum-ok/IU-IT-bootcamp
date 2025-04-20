from fastapi import APIRouter, Query

user_router = APIRouter(tags=['Users'])

@user_router.get('/user/')
async def get_user_info(login: str = Query(...), password: str = Query(...)):
    pass


@user_router.get('/users')
async def get_users_info():
    pass
