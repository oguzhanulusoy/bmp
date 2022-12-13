from django.urls import path
from . import views

API_HOME = "api/"
VIEW_HOME = "view/"

urlpatterns = [
    path(API_HOME + "get_user_list", views.get_user_list, name='get_user_list'),
    path(API_HOME + "get_user_by_email/<str:email>", views.get_user_by_email, name='get_user_by_email'),
    path(API_HOME + "get_user_by_pk/<str:pk>", views.get_user_by_pk, name= 'get_user_by_pk'),
]