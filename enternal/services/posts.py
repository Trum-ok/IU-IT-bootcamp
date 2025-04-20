from enternal.services.models.domains import Publication
from enternal.storages.sqlalchemy_db import db


async def get_post_by_id(post_id: str) -> Publication | None:
    return await db.get_publication(post_id)


async def get_posts() -> list[Publication]:
    return await db.get_publications()


async def create_post(post: Publication) -> None:
    return await db.add_publication(
        title=post.title,
        content=post.content,
        image_url=post.main_image_url,
        author_id=post.author,
        created_at=post.created_at
    )


async def update_post(updated_post: Publication) -> None:
    return await db.update_publication(
        title=updated_post.title,
        content=updated_post.content,
        image_url=updated_post.main_image_url,
        author_id=updated_post.author,
        created_at=updated_post.created_at
    )


async def delete_post(post_id: str) -> None:
    await db.remove_publication(post_id)
