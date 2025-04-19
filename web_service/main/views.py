import json
import uuid
import bcrypt
from django.conf import settings
from django.shortcuts import HttpResponse, render
from main.decorators import role_required
from minio import Minio
from minio.error import S3Error

def view_index(request):
    """Главная страница"""
    data = {
        "posts": [
            {
                "name": "test",
                "descript": "test"
            }
        ],
        "images": []
    }

    minio_client = Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_USE_HTTPS
    )
    try:
        objects = minio_client.list_objects(
            settings.MINIO_BUCKET_NAME,
            prefix="organizations/"
        )

        for obj in objects:

            image_url = minio_client.presigned_get_object(
                settings.MINIO_BUCKET_NAME,
                obj.object_name
            )

            data["images"].append({"url": image_url})

    except S3Error as exc:
        print("Ошибка при получении изображений из MinIO:", exc)

    if not request.session:
        data = {
            "user_id": request.session["id"],
            "user_role": request.session["role"],
        }
    return render(request, "index.html", context=data)


def search_posts(request):
    """Страница поиска публикаций"""
    return render(request, "searching_page.html")


def view_post(request, post_id):
    """Страница публикации"""
    if request.method == 'POST':
        temp_data = []
        posts = json.dumps(temp_data[post_id], ensure_ascii=False)

    return render(request, "post.html")


@role_required('writer')
def create_post(request):
    """Страница создания публикации"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        print(title, content)
        # отправляем запрос на сервер на создание публикации

    return render(request, "create_post.html")


@role_required('writer')
def delete_post(request):
    """Удаление поста"""
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        print(post_id)
        # запрос на удаление поста по id
    return HttpResponse("Ok")


@role_required('writer')
def update_post(request):
    """Страница обновления публикации."""
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        title = request.POST.get('title')
        content = request.POST.get('content')

        # update_post_by_id
    return HttpResponse("Ok")


@role_required('moderator')
def create_organization(request):
    """Создание организации с загрузкой изображения в MinIO"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        print(name, description)

        image = request.FILES.get('image')
        if image:
            try:
                minio_client = Minio(
                    settings.MINIO_ENDPOINT,
                    access_key=settings.MINIO_ACCESS_KEY,
                    secret_key=settings.MINIO_SECRET_KEY,
                    secure=settings.MINIO_USE_HTTPS
                )

                # Генерируем уникальное имя файла
                file_name = f"organizations/{uuid.uuid4()}_{image.name}"

                # Проверяем и создаем бакет если нужно
                if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
                    minio_client.make_bucket(settings.MINIO_BUCKET_NAME)

                # Загружаем файл
                minio_client.put_object(
                    settings.MINIO_BUCKET_NAME,
                    file_name,
                    image,
                    length=image.size,
                    content_type=image.content_type
                )

                print(f"Изображение загружено: {file_name}")
                # Здесь можно сохранить file_name в базу данных

            except S3Error as exc:
                print("Ошибка MinIO:", exc)
                return render(request, "create_organization.html", {
                    'error': 'Ошибка при загрузке изображения'
                })
    return render(request, "create_organization.html")


@role_required('moderator')
def delete_organization(request):
    """Удаление организации"""
    if request.method == 'POST':
        organization_id = request.POST.get('organization_id')
        # удаление организации по id
        print(organization_id)

    return HttpResponse("Ok")


def view_organizations(request):
    """Просмотр всех доступных организаций"""
    data = {
        "organizations": [
            {
                "name": "test",
                "descript": "test"
            }
        ]
    }
    # get_all_organizations
    return render(request, "organization.html")


@role_required('moderator')
def create_writer(request):
    """Создание писателя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        organization = request.POST.get('organization')
        password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt(rounds=12)
        )
        print(username, password, organization)
    return render(request, "create_writer.html")


@role_required('moderator')
def delete_writer(request):
    """Удаления писателя"""
    if request.method == 'POST':
        user_id = request.POST.get('id')
        print(user_id)
    return HttpResponse("Ok")
