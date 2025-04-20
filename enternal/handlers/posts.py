from fastapi import APIRouter
from services.domains import Publication
from services.posts import get_posts, get_post_by_id, create_post, update_post, delete_post

post_router = APIRouter()

@post_router.get('/posts/')
async def handler_get_all_posts():
    return await get_posts()


@post_router.get('/post_by_id/')
async def handler_get_post_by_id(post: Publication):
    return await get_post_by_id(post.id)


@post_router.post('/posts/create')
async def handler_create_post(post: Publication):
    await create_post(post)


@post_router.patch('/posts/update')
async def update_post(post: Publication):
    await update_post(post)


@post_router.delete('/posts/delete')
async def delete_post(post: Publication):
    await delete_post(post)
