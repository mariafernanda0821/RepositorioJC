#
from django.urls import path

from . import views

app_name = "users_app"

urlpatterns = [
    path(
        'users/register/', 
        views.UserRegisterView.as_view(),
        name='user-register',
    ),
]