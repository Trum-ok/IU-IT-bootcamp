from fastapi import APIRouter

router = APIRouter()

@router.get("/posts")
async def get_posts():
    return {
        'Cause they feel so empty without me'
    }
