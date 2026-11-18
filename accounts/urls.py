from django.urls import path

from . import api, views

urlpatterns = [
    path("auth/login/", api.sign_in, name="api-login"),
    path("auth/logout/", api.sign_out, name="api-logout"),
    path("users/", api.user_create, name="api-user-create"),
    path("users/<int:user_id>/", api.user_update, name="api-user-update"),
    path("login/", views.sign_in, name="login"),
    path("logout/", views.sign_out, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("settings/", views.settings_view, name="settings"),
    path("manage/users/", views.user_management, name="user-management"),
    path("manage/users/<int:user_id>/update/", views.update_user, name="user-update"),
    path(
        "manage/users/<int:user_id>/deactivate/",
        views.deactivate_user,
        name="user-deactivate",
    ),
]
