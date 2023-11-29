from django.urls import path
from . import views

urlpatterns = [
    path('add_photo', views.add_photo),
    path('add_user', views.add_user),
    path('user_login', views.user_login),
    path('change_password', views.change_password),
    path('add_book', views.add_book),
    path('add_favourite', views.add_favourite),
    path('add_score', views.add_score),
    path('add_bookComment', views.add_bookComment),
    path('add_community', views.add_community),
    path('add_tip', views.add_tip),
    path('add_comment', views.add_comment),
    path('add_label', views.add_label),

]
