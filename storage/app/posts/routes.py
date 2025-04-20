import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.posts.views import (
        CompaniesListView,
        CompanyView,
        PublicationCreateView,
        PublicationDeleteView,
        PublicationsListView,
        PublicationUpdateView,
        PublicationView,
        UserByLoginView,
        UserCreateView,
        UserDeleteView,
        UsersListView,
        UserView,
    )

    app.router.add_view("/posts.", CompaniesListView)
    app.router.add_view("/posts.", CompanyView)
    app.router.add_view("/posts.", PublicationCreateView)
    app.router.add_view("/posts.", PublicationDeleteView)
    app.router.add_view("/posts.", PublicationsListView)
    app.router.add_view("/posts.", PublicationUpdateView)
    app.router.add_view("/posts.", PublicationView)
    app.router.add_view("/posts.", UserByLoginView)
    app.router.add_view("/posts.", UserCreateView)
    app.router.add_view("/posts.", UserDeleteView)
    app.router.add_view("/posts.", UsersListView)
    app.router.add_view("/posts.", UserView)


# urlpatterns = [
#     path('', views.view_index, name='home'),
#     path('posts/search/', views.search_posts, name='search_posts'),
#     path('posts/<str:post_id>/', views.view_post, name='view_post'),
#     path('posts/create/', views.create_post, name='create_post'),
#     path('posts/delete/', views.delete_post, name='delete_post'),
#     path('posts/update/<str:post_id>/', views.update_post, name='update_post'),

#     path('organizations/create/', views.create_organization,
#          name='create_organization'),
#     path('organizations/delete/',
#          views.delete_organization, name='delete_organization'),
#     path('organizations/', views.view_organizations, name='organizations_list'),

#     path('writer/create/', views.create_writer, name="create_writer"),
#     path('writer/delete/', views.delete_writer, name="delete_writer"),
#     path('writer/login/', writer_login, name='writer_login'),
#     path('moderator/login/', moderator_login, name='moderator_login'),

#     path('logout/', logout, name='logout'),
# ]
