from fastapi import APIRouter
from services.domains import Subscriber

subscriber_router = APIRouter(tags=['Subscribers'])

@subscriber_router.get('/get_subscriber_by_id')
async def get_subscriber(user: Subscriber):
    return {
        'id': user.id,
        'telegram_id': user.telegram_id,
        'subscriptions': user.subscriptions
    }


@subscriber_router.get('/get_subscriber_by_tg_id')
async def get_subscriber(user: Subscriber):
    return {
        'id': user.id,
        'telegram_id': user.telegram_id,
        'subscriptions': user.subscriptions
    }


@subscriber_router.post('/add_subscriber')
async def add_subscriber(user: Subscriber):
    return {
        'id': user.id,
        'telegram_id': user.telegram_id,
        'subscriptions': user.subscriptions
    }


@subscriber_router.delete('/remove_subscriber')
async def remove_subscriber(user: Subscriber):
    return {
        'id': user.id,
        'telegram_id': user.telegram_id,
        'subscriptions': user.subscriptions
    }
