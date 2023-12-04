from django.urls import path
from . import views

urlpatterns = [
    # path('add_photo', views.add_photo),
    path('add_user', views.add_user),
    path('check_user', views.check_user),
    path('get_userList', views.get_userList),
    path('get_userLogList', views.get_userLogList),
    path('user_login', views.user_login),
    path('change_password', views.change_password),
    path('modify_userdata', views.modify_user),
    path('modify_userPrivilege', views.modify_userPrivilege),
    path('get_bookInfo', views.get_bookInfo),
    path('get_books', views.getBookList),
    path('getIdOfBook', views.getIdOfBook),
    path('getRecommendedBooks', views.getRecommendedBooks),
    path('get_bookDetailList', views.get_bookDetailList),
    path('add_book', views.add_book),
    path('upload_book', views.upload_book),
    path('dig_book', views.dig_book),
    path('check_book', views.check_book),
    path('delete_book', views.delete_book),
    path('edit_book', views.edit_book),
    path('add_favourite', views.add_favourite),
    path('remove_favourite', views.remove_favourite),
    path('add_score', views.add_score),
    path('add_bookComment', views.add_bookComment),
    path('add_community', views.add_community),
    path('delete_community', views.delete_community),
    path('get_communities', views.get_communityList),
    path('check_community', views.check_community),
    path('add_tip', views.add_tip),
    path('delete_tip', views.delete_tip),
    path('add_support', views.add_support),
    path('add_unsupported', views.add_unsupported),
    path('get_tipList', views.get_tipList),
    path('get_tip_status', views.get_tip_status),
    path('accept_tip', views.acceptTip),
    path('refuse_tip', views.refuseTip),
    path('getTipsByFavor', views.getTipsByFavor),
    path('getTipsByComments', views.getTipsByComments),
    path('get_task', views.get_task),
    path('add_comment', views.add_comment),
    path('delete_comment', views.delete_comment),
    path('get_commentList', views.get_commentList),
    path('add_label', views.add_label),
    path('upload', views.upload),
    path('downLoad_books', views.downLoad_books)
]
