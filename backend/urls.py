from django.urls import path
from . import views

urlpatterns = [
    # path('add_photo', views.add_photo),
    path('add_user', views.add_user),
    path('check_user', views.check_user),
    path('user_login', views.user_login),
    path('change_password', views.change_password),
    path('modify_userdata', views.modify_user),
    path('get_bookInfo', views.get_bookInfo),
    path('get_books', views.getBookList),
    path('get_bookDetailList', views.get_bookDetailList),
    path('add_book', views.add_book),
    path('dig_book', views.dig_book),
    path('check_book', views.check_book),
    path('add_favourite', views.add_favourite),
    path('remove_favourite', views.remove_favourite),
    path('add_score', views.add_score),
    path('add_bookComment', views.add_bookComment),
    path('add_community', views.add_community),
    path('delete_community', views.delete_community),
    path('get_communities', views.get_communityList),
    path('check_community', views.check_community),
    path('add_tip', views.add_tip),
    path('get_tipList', views.get_tipList),
    path('add_comment', views.add_comment),
    path('add_label', views.add_label),
    path('upload', views.upload)

]
