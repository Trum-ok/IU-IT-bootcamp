from fastapi import APIRouter, Query

org_router = APIRouter(tags=['Organizations'])

@org_router.get('/organizations/')
async def get_all_organizations():
    pass
