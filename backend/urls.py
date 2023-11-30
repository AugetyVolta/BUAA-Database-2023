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
    path('get_books', views.BooksListAPIView.as_view()),
    path('add_book', views.add_book),
    path('add_favourite', views.add_favourite),
    path('add_score', views.add_score),
    path('add_bookComment', views.add_bookComment),
    path('add_community', views.add_community),
    path('add_tip', views.add_tip),
    path('add_comment', views.add_comment),
    path('add_label', views.add_label),

]
