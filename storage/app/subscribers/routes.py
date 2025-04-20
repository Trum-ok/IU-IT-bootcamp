import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.subscribers.views import (
        AddSubscriberView,
        CompanyView,
        SubscriberByIdView,
        SubscriberByTgIdView,
        SubscriberDeleteView,
        SubscriptionDeleteView,
    )

    app.router.add_view("/subs.get_by_id", SubscriberByIdView)
    app.router.add_view("/subs.get_by_tg_id", SubscriberByTgIdView)
    app.router.add_view("/subs.add_subscriber", AddSubscriberView)
    app.router.add_view("/subs.get_company", CompanyView)
    app.router.add_view("/subs.delete_user", SubscriberDeleteView)
    app.router.add_view("/subs.remove_subscription", SubscriptionDeleteView)
