from fastapi import APIRouter

main_router = APIRouter()


@main_router.get("/posts")
async def get_posts():
    return {
        'Cause they feel so empty without me'
    }
