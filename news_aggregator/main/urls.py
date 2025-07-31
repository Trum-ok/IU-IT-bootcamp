from django.urls import path

from main import views
from main.auth_views import logout, moderator_login, writer_login

urlpatterns = [
    path("", views.view_index, name="home"),
    path("posts/search/", views.search_posts, name="search_posts"),
    path("posts/storage/<str:post_id>/", views.view_post, name="view_post"),
    path("posts/create/", views.create_post, name="create_post"),
    path("posts/delete/", views.delete_post, name="delete_post"),
    path("posts/update/<str:post_id>/", views.update_post, name="update_post"),
    path("organizations/", views.view_organizations, name="organizations_list"),
    path("writer/create/", views.create_writer, name="create_writer"),
    path("writer/delete/", views.delete_writer, name="delete_writer"),
    path("writer/login/", writer_login, name="writer_login"),
    path("moderator/login/", moderator_login, name="moderator_login"),
    path("logout/", logout, name="logout"),
    path("authorization/", views.authorization, name="authorization"),
]
