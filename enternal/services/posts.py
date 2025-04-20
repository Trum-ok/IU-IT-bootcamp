from typing import Optional

from domains import Publication, User


def get_post_by_id(post_id: str) -> Optional["Publication"]:
    """Получение публикации по ID"""


def get_posts_by_author(author: "User") -> list["Publication"]:
    """Получение публикаций конкретного автора"""


def create_post(publication_data: "Publication") -> "Publication":
    """Создание новой публикации"""


def update_post(post_id: str, update_data: dict) -> "Publication":
    """Обновление существующей публикации"""


def delete_post(post_id: str) -> bool:
    """Удаление публикации"""


def search_posts(query: str) -> list["Publication"]:
    """Поиск публикаций по текстовому запросу"""
