from marshmallow import EXCLUDE, Schema, fields, validate


class PublicationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    main_image_url = fields.Str(required=True)
    created_at = fields.DateTime(required=True)

    # Foreign keys
    author_id = fields.Str(required=True)

    # Relationships
    author = fields.Nested("UserSchema", exclude=("publications", "company"))


class CompanySchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    image_url = fields.Str(required=True)

    # Relationships
    authors = fields.List(
        fields.Nested("UserSchema", exclude=("company", "publications"))
    )
    subscriptions = fields.List(
        fields.Nested("SubscriptionSchema", exclude=("company",))
    )


class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=True)
    login = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(
        required=True, validate=validate.OneOf(["author", "moderator", "admin"])
    )
    company_id = fields.Str(allow_none=True)

    # Relationships
    company = fields.Nested(CompanySchema, exclude=("authors", "subscriptions"))
    publications = fields.List(
        fields.Nested(PublicationSchema, exclude=("author",))
    )


class SubscriberSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(required=True)
    telegram_id = fields.Str(required=True)

    # Relationships
    subscriptions = fields.List(
        fields.Nested("SubscriptionSchema", exclude=("subscriber",))
    )


class SubscriptionSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(required=True)
    subscriber_id = fields.Int(required=True)
    company_id = fields.Str(required=True)

    # Relationships
    subscriber = fields.Nested(SubscriberSchema, exclude=("subscriptions",))
    company = fields.Nested(CompanySchema, exclude=("subscriptions", "authors"))


class PublicationCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    content = fields.Str(required=True)
    main_image_url = fields.Str(required=True, validate=validate.URL())
    author_id = fields.Str(required=True)


class UserCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    login = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str(
        required=True, validate=validate.OneOf(["author", "moderator", "admin"])
    )
    company_id = fields.Str(allow_none=True)


class SubscriptionCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    subscriber_id = fields.Int(required=True)
    company_id = fields.Str(required=True)
