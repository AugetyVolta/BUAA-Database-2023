import datetime

import jwt
from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import generics

from backend.filters import BooksFilter
from backend.models import Book, Community, User, Photo, Favourite, Score, BookComment, UserBookRelation, Tip, Label, \
    BookLabelRelation, OwnedCommunity, Comment
from backend.seralizers import BooksSerializer
from django.core import serializers


# Create your views here.
# # 添加照片
# def add_photo(request):
#     res = {"code": 400, "message": "", "data": None}
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             photo = Photo(path=data.get('path'))
#             photo.save()
#             res["code"] = 200
#             res["message"] = "success"
#             print('-------------------add_photo-------------------')
#         except Exception as e:
#             res["code"] = 500
#             res["message"] = "服务器错误：图片创建失败" + str(e)
#     else:
#         res["message"] = "请使用POST方法"
#     return JsonResponse(res)


# 创建用户
def add_user(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = User(account=data.get('account'),
                        nickname=data.get('nickname'),
                        password=data.get('password'),
                        gender=data.get('gender'),
                        age=data.get('age'))
            user.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_user-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：用户创建失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def check_user(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        account = request.GET.get("account")
        data = User.objects.filter(account=account).values().first()
        if not data:
            res['message'] = '用户账号可用'
            res['code'] = 200
        else:
            res['message'] = "用户已注册"
    except Exception as e:
        res['message'] = '服务器错误：' + str(e)
        res['code'] = 500
    return JsonResponse(res)


# 登录
def user_login(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        data = json.loads(request.body)
        user = User.objects.filter(account=data.get('account')).values().first()
        if user and user['account']:
            password = data.get('password')
            if password == user['password']:
                res["code"] = 200
                res["message"] = "success"
                user_data = {'id': user['id'], 'account': user['account'], 'nickname': user['nickname'],
                             'gender': user['gender'], 'age': user['age']}
                response_data = {"user_data": user_data, "token": user_data}
                res["data"] = response_data
                print('-------------------user_login-------------------')
            else:
                res['message'] = "密码输入错误"
        else:
            res["message"] = "用户不存在"
    except Exception as e:
        res["message"] = "服务器错误，错误原因：" + str(e)
        res["code"] = 500
    return JsonResponse(res)


def change_password(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.filter(account=data["user_account"]).values().first()
            old_password = data["old_password"]
            if old_password == user['password']:
                User.objects.filter(account=data['user_account']).update(password=data['new_password'])
                res['code'] = 200
                res['message'] = '修改成功'
                print('-------------------change_password-------------------')
            else:
                res['message'] = '原始密码错误'
        except Exception as e:
            res['code'] = 500
            res["message"] = "服务器错误：" + str(e)
    else:
        res['message'] = '请使用POST方式提交'
    return JsonResponse(res)


def modify_user(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            User.objects.filter(account=data["account"]).update(nickname=data.get('nickname'),
                                                                age=data.get('age'),
                                                                gender=data.get('gender'))
            res_data = User.objects.filter(account=data['account']).values().first()
            res["code"] = 200
            res['message'] = '更新成功'
            res['data'] = res_data
            print('-------------------modify_user-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


# 添加书籍
def add_book(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            book = Book(name=data.get('name'),
                        author=data.get('author'),
                        description=data.get('description'),
                        pic_url=data.get('pic_url'))
            book.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_book-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：书籍添加失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def getBookList(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        book_name = request.GET.get('name')
        if book_name == '':
            books = Book.objects.all().order_by("id")
        else:
            books = Book.objects.filter(name=book_name).order_by("id")
        res['data'] = []
        data_item = {"id": 0, "name": "", "pic_url": "", "description": ""}
        for book in books:
            data_item['id'] = book.id
            data_item['name'] = book.name
            data_item['pic_url'] = book.pic_url
            data_item['description'] = book.description
            res['data'].append(data_item)
            data_item = {"id": 0, "name": "", "pic_url": "", "description": ""}
        res["code"] = 200
        res["message"] = "success"

    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：" + str(e)
    return JsonResponse(res)


def get_bookInfo(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        data = {"content": [], "pic_url": "", "title": "", "author": "", "introduce": "", 'label': [],
                "average_score": 0.0}
        book = Book.objects.filter(id=request.GET.get('id')).values().first()
        data['introduce'] = book['description']
        data['pic_url'] = book['pic_url']
        data['title'] = book['name']
        data['author'] = book['author']
        # 平均打分
        data['average_score'] = '%.1f' % Score.objects.filter(book_id=request.GET.get('id')).aggregate(
            Avg('score')).get(
            'score__avg') if Score.objects.filter(book_id=request.GET.get('id')) else 0
        # 书籍label
        data['label'] = []
        bookLabelRelation_dict = BookLabelRelation.objects.filter(book=request.GET.get('id')).values('label')
        for item in bookLabelRelation_dict:
            label_id = item['label']
            data['label'].append(Label.objects.get(id=label_id).content)
        # 评论内容
        data['content'] = []
        content_item = {"name": "", "content_arr": [], "score": 0.0, "create_time": ""}
        book_comment_dict = BookComment.objects.filter(commented_book=request.GET.get('id')).order_by(
            '-create_time').values('id', 'content', 'create_time')
        for item in book_comment_dict:
            content_item["content_arr"].append(item['content'])
            # 评论对应的id
            book_comment_id = item['id']
            # 书评对应的用户id
            user_id = UserBookRelation.objects.get(comment=book_comment_id).user.id
            # 创建时间
            content_item["create_time"] = item['create_time']
            # 找到对应的用户名
            content_item["name"] = User.objects.get(id=user_id).nickname
            # 找到用户的评分
            content_item["score"] = Score.objects.filter(user=User.objects.get(id=user_id),
                                                         book=Book.objects.get(id=request.GET.get(
                                                             'id'))).first().score if Score.objects.filter(
                user=User.objects.get(id=user_id), book=Book.objects.get(id=request.GET.get('id'))) else 0
            data['content'].append(content_item)
            content_item = {"name": "", "content_arr": [], "score": 0.0, "create_time": ""}
        res["code"] = 200
        res["message"] = "success"
        res["data"] = data
        print('-------------------get_bookInfo-------------------')
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：" + str(e)
    finally:
        return JsonResponse(res)


# 添加收藏
def add_favourite(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 获得书评的用户
            user = User.objects.get(id=data.get('user_id'))
            # 获得被评论的书籍
            book = Book.objects.get(id=data.get('book_id'))
            favourite = Favourite(user=user,
                                  book=book)
            favourite.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_favourite-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：收藏失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


# 取消收藏
def remove_favourite(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 获得书评的用户
            user = User.objects.get(id=data.get('user_id'))
            # 获得被评论的书籍
            book = Book.objects.get(id=data.get('book_id'))
            Favourite.objects.filter(user=user,
                                     book=book).delete()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------remove_favourite-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：取消收藏失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


# 添加评分
def add_score(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 评分的用户
            user = User.objects.get(id=data.get('user_id'))
            # 获得被评分的书籍
            book = Book.objects.get(id=data.get('book_id'))
            score = Score(score=data.get('score'),
                          user=user,
                          book=book)
            score.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_score-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：评分失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


# 添加书评
def add_bookComment(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 获得被评价的书籍
            book = Book.objects.get(id=data.get('book_id'))
            book_comment = BookComment(content=data.get('reviewContent'),
                                       commented_book=book)
            book_comment.save()
            # 将用户和书评加入到用户书评对应表中
            user = User.objects.get(id=data.get('user_id'))
            userBookRelation = UserBookRelation(
                user=user,
                comment=book_comment
            )
            userBookRelation.save()
            # 增加评分
            score = Score(score=data.get('starRating'),
                          user=user,
                          book=book)
            score.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_bookComment-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：书籍评价失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


# 创建圈子
def add_community(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            community = Community(
                tilte=data.get('title'),
                topic=data.get('topic'))
            community.save()
            # 加入到用户拥有圈子表中
            user = User.objects.get(id=data.get('user_id'))
            ownedCommunity = OwnedCommunity(user=user,
                                            community=community)
            ownedCommunity.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_community-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：创建圈子失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


# 创建帖子
def add_tip(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 获得所属圈子
            community = Community.objects.get(id=data.get('community_id'))
            # 获得发帖用户
            user = User.objects.get(id=data.get('user_id'))
            tip = Tip(content=data.get('content'),
                      community=community,
                      user=user)
            tip.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_tip-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：创建帖子失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


# 创建帖子评论
def add_comment(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tip = Tip.objects.get(id=data.get('tip_id'))
            post_user = User.objects.get(id=data.get('user_id'))
            comment = Comment(content=data.get('content'),
                              post_user=post_user,
                              tip=tip)
            comment.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_comment-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：创建帖子评论失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


# 创建标签
def add_label(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            label = Label(content=data.get('content'))
            label.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_label-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：创建标签失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def add_bookLabelRelation(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 找到对应书籍
            book = Book.objects.get(id=data.get('book_id'))
            # 找到对应标签
            label = Label.objects.get(id=data.get('label_id'))
            bookLabelRelation = BookLabelRelation(book=book,
                                                  label=label)
            bookLabelRelation.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_bookLabelRelation-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：创建标签书籍对应记录失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)
