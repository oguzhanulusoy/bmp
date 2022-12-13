from django.urls import path
from . import views

API_HOME = "api/"
VIEW_HOME = "view/"

urlpatterns = [
    path(API_HOME + "get_user_list", views.get_user_list, name='get_user_list'),
]