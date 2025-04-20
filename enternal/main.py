from fastapi import FastAPI

from handlers.main import router

app = FastAPI()

app.include_router(router)
