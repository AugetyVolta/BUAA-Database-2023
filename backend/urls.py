from django.urls import path
from . import views

urlpatterns = [
    path('create_user', views.create_user)  # http://127.0.0.1:8000/api/create_user

]
