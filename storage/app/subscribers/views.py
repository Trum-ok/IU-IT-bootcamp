import json

from aiohttp.web import HTTPNotFound
from aiohttp.web_response import Response
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from storage.app.models import Company, Subscriber, Subscription
from storage.app.schemas import CompanySchema, SubscriberSchema

from app.base.base_accessor import BaseAccessor
from app.web.app import View
from app.web.schemes import ErrorResponseSchema, OkResponseSchema
from app.web.utils import json_response

__all__ = (
    "AddSubscriberView",
    "CompanyView",
    "SubscriberByIdView",
    "SubscriberByTgIdView",
    "SubscriberDeleteView",
)


class SubscriberByIdView(View):
    @docs(tags=["subscribers"], summary="Get subscriber by ID")
    @response_schema(SubscriberSchema, 200)
    @response_schema(ErrorResponseSchema, 404)
    @BaseAccessor.connection
    async def get(self, id_: int, *, session: AsyncSession) -> Response:
        stmt = select(Subscriber).where(Subscriber.id == id_)
        result = await session.execute(stmt)
        subscriber = result.scalar_one_or_none()

        if not subscriber:
            raise HTTPNotFound(
                text=json.dumps({"error": "Subscriber not found"}),
                content_type="application/json",
            )

        return json_response(data=SubscriberSchema().dump(subscriber))


class SubscriberByTgIdView(View):
    @docs(tags=["subscribers"], summary="Get subscriber by Telegram ID")
    @response_schema(SubscriberSchema, 200)
    @response_schema(ErrorResponseSchema, 404)
    @BaseAccessor.connection
    async def get(self, tg_id: str, *, session: AsyncSession) -> Response:
        stmt = select(Subscriber).where(Subscriber.telegram_id == tg_id)
        result = await session.execute(stmt)
        subscriber = result.scalar_one_or_none()

        if not subscriber:
            raise HTTPNotFound(
                text=json.dumps({"error": "Subscriber not found"}),
                content_type="application/json",
            )

        return json_response(data=SubscriberSchema().dump(subscriber))


class AddSubscriberView(View):
    @docs(tags=["subscribers"], summary="Add new subscriber")
    @request_schema(SubscriberSchema)
    @response_schema(SubscriberSchema, 201)
    @response_schema(ErrorResponseSchema, 400)
    @BaseAccessor.connection
    async def post(self, tg_id: int, *, session: AsyncSession) -> Response:
        try:
            subscriber = Subscriber(telegram_id=str(tg_id))
            session.add(subscriber)
            await session.commit()
        except IntegrityError:
            await session.rollback()
            return await session.get(Subscriber, str(tg_id))

        subscriber_dict = {
            "id": subscriber.id,
            "telegram_id": subscriber.telegram_id,
            # TODO
        }
        return json_response(subscriber_dict)


class CompanyView(View):
    @docs(tags=["companies"], summary="Get company by ID")
    @response_schema(CompanySchema, 200)
    @response_schema(ErrorResponseSchema, 404)
    @BaseAccessor.connection
    async def get(self, id: str, *, session: AsyncSession) -> Response:
        company = await session.scalar(select(Company).where(Company.id == id))

        if not company:
            raise HTTPNotFound(
                text=json.dumps({"error": "Company not found"}),
                content_type="application/json",
            )

        return json_response(data=CompanySchema().dump(company))


class SubscriberDeleteView(View):
    @docs(tags=["subscribers"], summary="Delete subscriber")
    @response_schema(OkResponseSchema, 200)
    @response_schema(ErrorResponseSchema, 404)
    @BaseAccessor.connection
    async def delete(
        self, telegram_id: str, *, session: AsyncSession
    ) -> Response:
        subscriber = await session.scalar(
            select(Subscriber).where(Subscriber.telegram_id == telegram_id)
        )

        if not subscriber:
            raise HTTPNotFound(
                text=json.dumps(
                    {"error": f"Subscriber [{telegram_id}] not found"}
                ),
                content_type="application/json",
            )

        await session.execute(
            delete(Subscription).where(
                Subscription.subscriber_id == subscriber.id
            )
        )

        await session.delete(subscriber)
        await session.commit()

        return json_response(
            data={"status": "ok", "message": "Subscriber deleted"}
        )


class SubscriptionDeleteView(View):
    @docs(tags=["subscriptions"], summary="Remove subscription")
    @response_schema(OkResponseSchema, 200)
    @response_schema(ErrorResponseSchema, 404)
    @BaseAccessor.connection
    async def delete(
        self, telegram_id: str, company_id: str, *, session: AsyncSession
    ) -> Response:
        subscriber = await session.scalar(
            select(Subscriber).where(Subscriber.telegram_id == telegram_id)
        )
        if not subscriber:
            raise HTTPNotFound(
                text=json.dumps(
                    {"error": f"Subscriber [{telegram_id}] not found"}
                ),
                content_type="application/json",
            )

        company = await session.scalar(
            select(Company).where(Company.id == company_id)
        )
        if not company:
            raise HTTPNotFound(
                text=json.dumps({"error": f"Company [{company_id}] not found"}),
                content_type="application/json",
            )

        result = await session.execute(
            delete(Subscription).where(
                Subscription.subscriber_id == subscriber.id,
                Subscription.company_id == company.id,
            )
        )

        if result.rowcount == 0:
            raise HTTPNotFound(
                text=json.dumps({"error": "Subscription not found"}),
                content_type="application/json",
            )

        await session.commit()

        return json_response(
            data={"status": "ok", "message": "Subscription removed"}
        )
