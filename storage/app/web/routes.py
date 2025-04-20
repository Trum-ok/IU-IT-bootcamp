from aiohttp.web_app import Application


def setup_routes(app: Application):
    from app.subscribers.routes import setup_routes as subs_setup_routes

    subs_setup_routes(app)
