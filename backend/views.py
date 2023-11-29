import datetime

import jwt
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from backend.models import Book, Community, User, Photo, Favourite, Score, BookComment, UserBookRelation, Tip, Label, \
    BookLabelRelation, OwnedCommunity, Comment


# Create your views here.
# 添加照片
def add_photo(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            photo = Photo(path=data.get('path'))
            photo.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_photo-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：图片创建失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


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
            # 获得书籍对应的图片
            photo = Photo.objects.get(id=data.get('photo_id'))
            book = Book(name=data.get('name'),
                        author=data.get('author'),
                        description=data.get('description'),
                        describe_photo=photo)
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
            book_comment = BookComment(content=data.get("content"),
                                       commented_book=book)
            book_comment.save()
            # 将用户和书评加入到用户书评对应表中
            user = User.objects.get(id=data.get('user_id'))
            userBookRelation = UserBookRelation(
                user=user,
                comment=book_comment
            )
            userBookRelation.save()
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
