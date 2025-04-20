from fastapi import APIRouter
from services.domains import Company

org_router = APIRouter(tags=['Organizations'])

@org_router.get('/organizations/')
async def get_all_organizations():
    pass


@org_router.post('/organizations/create')
async def create_organization(organization: Company):
    return {
        'id': organization.id,
        'desc': organization.description,
        'image_url': organization.image_url,
        'authors': organization.authors,
        'subscriptions': organization.subscriptions
    }


@org_router.delete('/organization/delete')
async def delete_organization(organization: Company):
    return {
        'id': organization.id,
        'desc': organization.description,
        'image_url': organization.image_url,
        'authors': organization.authors,
        'subscriptions': organization.subscriptions
    }
