import uuid
import requests

import bcrypt
from django.conf import settings
from django.shortcuts import HttpResponse, render, redirect

from main.decorators import role_required
from minio import Minio


ENCODING = "utf-8"
ROUNDS = 12


def view_index(request):
    """Главная страница"""
    minio_client = Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_USE_HTTPS,
    )

    data = {"posts": []}
    response = requests.get("http://127.0.0.1:9999/posts/")
    response_data = response.json()
    if response_data:
        for item in response_data:
            image_url = minio_client.presigned_get_object(
                settings.MINIO_BUCKET_NAME, item.image
            )

            data["posts"].append({
                'title': item.title,
                'content': item.content,
                'author_id': item.author_id,
                'image': image_url,
                'date': item.created_at
            })

    return render(request, "index.html", context=data)


def search_posts(request):
    """Страница поиска публикаций"""
    if request.method == "POST":
        search_data = request.POST.get("search_query")

    return redirect('home')


def view_post(request, post_id):
    """Страница публикации"""
    if request.method == "POST":
        params = {'id': post_id}
        response = requests.get(
            "http://127.0.0.1:9999/postspost_by_id/", params=params
        )
        response_data = response.json()
    return render(request, "post.html", context=response_data)


@role_required("writer")
def create_post(request):
    """Страница создания публикации"""
    if request.method == "POST":
        data = {
            "title": request.POST.get("title"),
            "content": request.POST.get("content")
        }

        image = request.FILES.get("image")
        if image:
            minio_client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_USE_HTTPS,
            )

            # Генерируем уникальное имя файла
            file_name = f"posts/{uuid.uuid4()}_{image.name}"

            # Проверяем и создаем бакет если нужно
            if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
                minio_client.make_bucket(settings.MINIO_BUCKET_NAME)

            # Загружаем файл
            minio_client.put_object(
                settings.MINIO_BUCKET_NAME,
                file_name,
                image,
                length=image.size,
                content_type=image.content_type,
            )
            data["image"] = file_name
        try:
            _ = requests.post(
                "http://127.0.0.1:9999/posts/create", data=data
            )
        except Exception:
            return HttpResponse("Ошибка создания публикации")
    return render(request, "create_post.html")


@role_required("writer")
def delete_post(request):
    """Удаление поста"""
    data = {"posts": []}
    response = requests.get("http://127.0.0.1:9999/posts/")
    response_data = response.json()
    if response_data:
        for item in response_data:
            data["posts"].append({
                'title': item.title
            })

    if request.method == "POST":
        post_id = request.POST.get("post_id")
        delete_data = {"id": post_id}
        _ = requests.post(
            "http://127.0.0.1:9999/posts/delete", data=delete_data
        )

    return render(request, "delete_post.html")


@role_required("writer")
def update_post(request):
    """Страница обновления публикации."""
    if request.method == "POST":
        data = {
            "title": request.POST.get("title"),
            "content": request.POST.get("content"),
            "author_id": request.POST.get("author_id"),
            "image": request.POST.get("image"),
            "date": request.POST.get("date")
        }
        _ = requests.post(
            "http://127.0.0.1:9999/posts/update", data=data
        )
    return HttpResponse("Ok")


def view_organizations(request):
    """Просмотр всех доступных организаций"""
    response = requests.get("http://127.0.0.1:9999/organizations/")
    response_data = response.json()
    return render(request, "organization.html", context=response_data)


@role_required("moderator")
def create_writer(request):
    """Создание писателя"""
    response = requests.get("http://127.0.0.1:9999/organizations/")
    response_data = response.json()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        organization = request.POST.get("organization")

        hashed_password = bcrypt.hashpw(
            password.encode(ENCODING), bcrypt.gensalt(rounds=ROUNDS)
        )

        print(username, hashed_password, organization)
    return render(request, "create_writer.html", context=response_data)


@role_required("moderator")
def delete_writer(request):
    """Удаления писателя"""
    if request.method == "POST":
        user_id = request.POST.get("id")
        print(user_id)
    return render(request, "delete_writer.html")


def authorization(request):
    return render(request, "authorization.html")
