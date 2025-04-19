from fastapi import APIRouter
from services.domains import Subscriber, Subscription

subscription_router = APIRouter(tags=['Subscriptions'])

@subscription_router.post('/add_subscription')
async def add_subscription(user: Subscriber):
    return {
        'id': user.id,
        'telegram_id': user.telegram_id,
        'subscriptions': user.subscriptions
    }


@subscription_router.delete('/remove_subscription')
async def remove_subscription(subscription: Subscription):
    return {
        'user': subscription.subscriber,
        'company': subscription.company
    }


@subscription_router.delete('/remove_all_subscriptions')
async def remove_subscription(subscription: Subscription):
    return {
        'user': subscription.subscriber,
        'company': subscription.company
    }
