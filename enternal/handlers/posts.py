from fastapi import APIRouter, Query
from services.domains import Publication

post_router = APIRouter()

@post_router.get('/posts/')
async def get_all_posts():
    pass


@post_router.get('/post_by_id/')
async def get_post_by_id(post: Publication):
    return {
        'title': post.title,
        'content': post.content,
        'author_id': post.author_id,
        'image': post.main_image_url,
        'date': post.created_at
    }


@post_router.post('/posts/create')
async def create_post(post: Publication):
    return {
        'title': post.title,
        'content': post.content,
        'author_id': post.author_id,
        'image': post.main_image_url,
        'date': post.created_at
    }


@post_router.patch('/posts/update')
async def update_post(post: Publication):
    return {
        'title': post.title,
        'content': post.content,
        'author_id': post.author_id,
        'image': post.main_image_url,
        'date': post.created_at
    }


@post_router.delete('/posts/delete')
async def delete_post(post: Publication):
    return {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author_id': post.author_id,
        'image': post.main_image_url,
        'date': post.created_at
    }
