import json
from uuid import uuid4

from aiohttp.web import HTTPConflict, HTTPNotFound
from aiohttp.web_response import Response
from aiohttp_apispec import docs, request_schema, response_schema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from storage.app.models import Company, Publication, User
from storage.app.schemas import (
    CompanySchema,
    PublicationCreateSchema,
    PublicationSchema,
    PublicationUpdateSchema,
    UserCreateSchema,
    UserSchema,
)

from app.base.base_accessor import BaseAccessor
from app.web.app import View
from app.web.schemes import ErrorResponseSchema, OkResponseSchema
from app.web.utils import json_response


class PublicationView(View):
    @docs(tags=["publications"], summary="Get publication by ID")
    @response_schema(PublicationSchema, 200)
    @response_schema(ErrorResponseSchema, 404)
    @BaseAccessor.connection
    async def get(
        self, publication_id: str, *, session: AsyncSession
    ) -> Response:
        stmt = select(Publication).where(Publication.id == publication_id)
        result = await session.execute(stmt)
        publication = result.scalar()

        if not publication:
            raise HTTPNotFound(
                text=json.dumps({"error": "Publication not found"}),
                content_type="application/json",
            )

        return json_response(data=PublicationSchema().dump(publication))


class PublicationsListView(View):
    @docs(tags=["publications"], summary="Get all publications")
    @response_schema(PublicationSchema(many=True), 200)
    @BaseAccessor.connection
    async def get(self, *, session: AsyncSession) -> Response:
        stmt = select(Publication)
        result = await session.execute(stmt)
        publications = result.scalars().all()
        return json_response(
            data=PublicationSchema(many=True).dump(publications)
        )


class PublicationCreateView(View):
    @docs(tags=["publications"], summary="Create new publication")
    @request_schema(PublicationCreateSchema)
    @response_schema(PublicationSchema, 201)
    @response_schema(ErrorResponseSchema, 400)
    @BaseAccessor.connection
    async def post(self, *, session: AsyncSession) -> Response:
        data = await self.request.json()
        schema = PublicationCreateSchema()
        validated_data = schema.load(data)

        publication_id = str(uuid4())
        publication = Publication(id=publication_id, **validated_data)

        session.add(publication)
        await session.commit()

        return json_response(
            data=PublicationSchema().dump(publication), status=201
        )


class PublicationUpdateView(View):
    @docs(tags=["publications"], summary="Update publication")
    @request_schema(PublicationUpdateSchema)
    @response_schema(PublicationSchema, 200)
    @response_schema(ErrorResponseSchema, 400)
    @response_schema(ErrorResponseSchema, 404)
    @BaseAccessor.connection
    async def patch(
        self, publication_id: str, *, session: AsyncSession
    ) -> Response:
        data = await self.request.json()
        schema = PublicationUpdateSchema()  # TODO
        validated_data = schema.load(data)

        stmt = select(Publication).where(Publication.id == publication_id)
        result = await session.execute(stmt)
        publication = result.scalar()

        if not publication:
            raise HTTPNotFound(
                text=json.dumps({"error": "Publication not found"}),
                content_type="application/json",
            )

        for key, value in validated_data.items():
            setattr(publication, key, value)

        session.add(publication)
        await session.commit()

        return json_response(data=PublicationSchema().dump(publication))


class PublicationDeleteView(View):
    @docs(tags=["publications"], summary="Delete publication")
    @response_schema(OkResponseSchema, 200)
    @response_schema(ErrorResponseSchema, 404)
    @BaseAccessor.connection
    async def delete(
        self, publication_id: str, *, session: AsyncSession
    ) -> Response:
        stmt = select(Publication).where(Publication.id == publication_id)
        result = await session.execute(stmt)
        publication = result.scalar()

        if not publication:
            raise HTTPNotFound(
                text=json.dumps({"error": "Publication not found"}),
                content_type="application/json",
            )

        await session.delete(publication)
        await session.commit()

        return json_response(
            data={"status": "ok", "message": "Publication deleted"}
        )


class CompanyView(View):
    @docs(tags=["companies"], summary="Get company by ID")
    @response_schema(CompanySchema, 200)
    @response_schema(ErrorResponseSchema, 404)
    @BaseAccessor.connection
    async def get(self, company_id: str, *, session: AsyncSession) -> Response:
        stmt = select(Company).where(Company.id == company_id)
        result = await session.execute(stmt)
        company = result.scalar()

        if not company:
            raise HTTPNotFound(
                text=json.dumps({"error": "Company not found"}),
                content_type="application/json",
            )

        return json_response(data=CompanySchema().dump(company))


class CompaniesListView(View):
    @docs(tags=["companies"], summary="Get all companies")
    @response_schema(CompanySchema(many=True), 200)
    @BaseAccessor.connection
    async def get(self, *, session: AsyncSession) -> Response:
        stmt = select(Company)
        result = await session.execute(stmt)
        companies = result.scalars().all()
        return json_response(data=CompanySchema(many=True).dump(companies))


class UserView(View):
    @docs(tags=["users"], summary="Get user by ID")
    @response_schema(UserSchema, 200)
    @response_schema(ErrorResponseSchema, 404)
    @BaseAccessor.connection
    async def get(self, user_id: str, *, session: AsyncSession) -> Response:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar()

        if not user:
            raise HTTPNotFound(
                text=json.dumps({"error": "User not found"}),
                content_type="application/json",
            )

        return json_response(data=UserSchema().dump(user))


class UserByLoginView(View):
    @docs(tags=["users"], summary="Get user by login")
    @response_schema(UserSchema, 200)
    @response_schema(ErrorResponseSchema, 404)
    @BaseAccessor.connection
    async def get(self, login: str, *, session: AsyncSession) -> Response:
        stmt = select(User).where(User.login == login)
        result = await session.execute(stmt)
        user = result.scalar()

        if not user:
            raise HTTPNotFound(
                text=json.dumps({"error": "User not found"}),
                content_type="application/json",
            )

        return json_response(data=UserSchema().dump(user))


class UsersListView(View):
    @docs(tags=["users"], summary="Get all users")
    @response_schema(UserSchema(many=True), 200)
    @BaseAccessor.connection
    async def get(self, *, session: AsyncSession) -> Response:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()
        return json_response(data=UserSchema(many=True).dump(users))


class UserCreateView(View):
    @docs(tags=["users"], summary="Create new user")
    @request_schema(UserCreateSchema)
    @response_schema(UserSchema, 201)
    @response_schema(ErrorResponseSchema, 400)
    @response_schema(ErrorResponseSchema, 409)
    @BaseAccessor.connection
    async def post(self, *, session: AsyncSession) -> Response:
        data = await self.request.json()
        schema = UserCreateSchema()

        validated_data = schema.load(data)

        stmt = select(User).where(User.login == validated_data["login"])
        result = await session.execute(stmt)
        if result.scalar():
            raise HTTPConflict(
                text=json.dumps({"error": "User already exists"}),
                content_type="application/json",
            )

        user_id = str(uuid4())
        user = User(id=user_id, **validated_data)

        session.add(user)
        await session.commit()

        return json_response(data=UserSchema().dump(user), status=201)


class UserDeleteView(View):
    @docs(tags=["users"], summary="Delete user")
    @response_schema(OkResponseSchema, 200)
    @response_schema(ErrorResponseSchema, 404)
    @BaseAccessor.connection
    async def delete(self, user_id: str, *, session: AsyncSession) -> Response:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar()

        if not user:
            raise HTTPNotFound(
                text=json.dumps({"error": "User not found"}),
                content_type="application/json",
            )

        await session.delete(user)
        await session.commit()

        return json_response(data={"status": "ok", "message": "User deleted"})
