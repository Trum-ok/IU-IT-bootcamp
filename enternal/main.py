from fastapi import FastAPI
from .handlers.users import user_router
from .handlers.organizations import org_router
from .handlers.posts import post_router
from .handlers.subscribers import subscriber_router
from .handlers.subscription import subscription_router

app = FastAPI()

app.include_router(user_router)
app.include_router(org_router)
app.include_router(post_router)
app.include_router(subscriber_router)
app.include_router(subscription_router)
