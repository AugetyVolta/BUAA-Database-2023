import os
from datetime import datetime
import jwt
import pandas as pd
from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import generics

from backend.DigBooks import dig_books
from backend.models import Book, Community, User, Photo, Favourite, Score, BookComment, UserBookRelation, Tip, Label, \
    BookLabelRelation, OwnedCommunity, Comment
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
            tags = data.get('tag')
            book = Book(name=data.get('name'),
                        author=data.get('author'),
                        description=data.get('introduction'),
                        pic_url=data.get('pic_url'))
            book.save()
            for tag in tags:
                label = Label.objects.get(content=tag)
                newRelation = BookLabelRelation(book=book, label=label)
                newRelation.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_book-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：书籍添加失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def check_book(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        book = Book.objects.filter(name=request.GET.get('name'),
                                   author=request.GET.get('author'))
        if not book:
            res["code"] = 200
            res["message"] = "书籍可用"
        else:
            res["code"] = 400
            res["message"] = "already exists"
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误:检查书籍失败" + str(e)
    return JsonResponse(res)


# 挖掘书籍并添加
def dig_book(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            book_data = dig_books()
            books_to_create = [Book(**data) for data in book_data]
            Book.objects.bulk_create(books_to_create)
            res['data'] = len(book_data)
            res["code"] = 200
            res["message"] = "success"
            print('-------------------dig_book-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：书籍爬取失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def delete_book(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            book = Book.objects.get(name=data.get('title'), author=data.get('author'))
            user_id = data.get('user_id')
            if user_id == 1:
                book.delete()
                res["code"] = 200
                res["message"] = "success"
            else:
                res["code"] = 400
                res["message"] = "fail"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：书籍删除失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def getBookList(request):
    res = {"code": 400, "message": "", "data": None, "total": 0}
    try:
        book_name = request.GET.get('name')
        # start_position = (int(request.GET.get('page')) - 1) * 10
        # count_to_fetch = int(request.GET.get('limit'))
        books = Book.objects.filter(name__icontains=book_name).order_by("id")
        res['data'] = []
        res['total'] = Book.objects.filter(name__icontains=book_name).count()
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


def get_bookDetailList(request):
    res = {"code": 400, "message": "", "data": None, "total": 0}
    try:
        start_position = (int(request.GET.get('page')) - 1) * 10
        count_to_fetch = int(request.GET.get('limit'))
        tag = request.GET.get('tag')
        books = Book.objects.filter(name__icontains=request.GET.get('title'),
                                    author__icontains=request.GET.get('author'),
                                    description__icontains=request.GET.get('introduction')).order_by("id")[
                start_position:start_position + count_to_fetch]
        res['data'] = []
        res['total'] = Book.objects.filter(name__icontains=request.GET.get('title'),
                                           author__icontains=request.GET.get('author'),
                                           description__icontains=request.GET.get('introduction')).count()
        data_item = {"id": 0, "title": "", "author": "", "introduction": "", "score": 0.0, "liked_times": 0, "tag": ""}
        for book in books:
            data_item['tag'] = ""
            bookLabelRelations = BookLabelRelation.objects.filter(book=book)
            for bookLabelRelation in bookLabelRelations:
                data_item['tag'] += bookLabelRelation.label.content + " "
            if tag in data_item['tag']:
                data_item['id'] = book.id
                data_item['title'] = book.name
                data_item['author'] = book.author
                data_item['introduction'] = book.description
                data_item['score'] = '%.1f' % Score.objects.filter(book_id=book.id).aggregate(
                    Avg('score')).get(
                    'score__avg') if Score.objects.filter(book_id=book.id) else 0
                data_item['liked_times'] = Favourite.objects.filter(book=book).count()
                res['data'].append(data_item)
            data_item = {"id": 0, "title": "", "author": "", "introduction": "", "score": 0.0, "liked_times": 0,
                         "tag": ""}
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
                "average_score": 0.0, "isBookFavorite": False}
        book = Book.objects.filter(id=request.GET.get('id')).values().first()
        user = User.objects.filter(id=request.GET.get('user_id')).first()
        data['introduce'] = book['description']
        data['pic_url'] = book['pic_url']
        data['title'] = book['name']
        data['author'] = book['author']
        # 是否被收藏
        data['isBookFavorite'] = True if Favourite.objects.filter(user=user, book=Book.objects.filter(
            id=request.GET.get('id')).first()) else False
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


def downLoad_books(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        books = Book.objects.all().order_by("id")
        res['data'] = []
        data_item = {"id": 0, "title": "", "author": "", "introduction": "", "score": 0.0, "liked_times": 0, "tag": ""}
        result = pd.DataFrame()
        for book in books:
            data_item['tag'] = ""
            bookLabelRelations = BookLabelRelation.objects.filter(book=book)
            for bookLabelRelation in bookLabelRelations:
                data_item['tag'] += bookLabelRelation.label.content + " "
            data_item['id'] = book.id
            data_item['title'] = book.name
            data_item['author'] = book.author
            data_item['introduction'] = book.description
            data_item['score'] = '%.1f' % Score.objects.filter(book_id=book.id).aggregate(
                Avg('score')).get(
                'score__avg') if Score.objects.filter(book_id=book.id) else 0
            data_item['liked_times'] = Favourite.objects.filter(book=book).count()
            cache = pd.DataFrame(
                {"id": [data_item['id']], "title": [data_item['title']], "author": [data_item['author']],
                 "introduction": [data_item['introduction']], "score": [data_item['score']],
                 "liked_times": [data_item['liked_times']],
                 "tag": [data_item['tag']]})
            result = pd.concat([result, cache])
            data_item = {"id": 0, "title": "", "author": "", "introduction": "", "score": 0.0, "liked_times": 0,
                         "tag": ""}
        result.head()
        result.to_excel('media\书籍信息.xlsx')
        res['data'] = "书籍信息.xlsx"
        res["code"] = 200
        res["message"] = "success"
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：" + str(e)
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


# 检查圈子是否存在
def check_community(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        title = request.GET.get("title")
        data = Community.objects.filter(title=title).values().first()
        if not data:
            res['message'] = '圈子名可用'
            res['code'] = 200
        else:
            res['message'] = "圈子已被创建，请重新输入"
    except Exception as e:
        res['message'] = '服务器错误：' + str(e)
        res['code'] = 500
    return JsonResponse(res)


# 创建圈子
def add_community(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            community = Community(
                title=data.get('name'),
                topic=data.get('introduction'))
            community.save()
            # 加入到用户拥有圈子表中
            print(data.get('user_id'))
            print(data.get('name'))
            print(data.get('introduction'))
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


def delete_community(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            community = Community.objects.get(title=data.get('name'))
            user = User.objects.get(id=data.get("user_id"))
            ownedCommunity = OwnedCommunity.objects.filter(user=user, community=community)
            if ownedCommunity:
                community.delete()
                res["code"] = 200
                res["message"] = "success"
            else:
                res["code"] = 400
                res["message"] = "fail"
            print('-------------------add_community-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：删除圈子失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


# 获得圈子
# def get_community(request):
#     res = {"code": 400, "message": "", "data": None}
#     try:
#         data = {"name": "", 'introduction': "", "tag": [], 'add_date': ""}
#         community = Community.objects.get(id=request.GET.get('community_id'))
#         data['name'] = community.title
#         data['introduction'] = community.topic
#         data['add_date'] = community.create_time
#         data['tag'] = ["dadads", "fdsfsdf"]
#         res["code"] = 200
#         res["message"] = "success"
#         res['data'] = data
#     except Exception as e:
#         res["code"] = 500
#         res["message"] = "服务器错误：" + str(e)
#     return JsonResponse(res)

# 获得圈子，带查找
def get_communityList(request):
    res = {"code": 400, "message": "", "data": None, "total": 0}
    try:
        res['data'] = []
        start_time = request.GET.get('startTime')
        end_time = request.GET.get('endTime')
        start_position = (int(request.GET.get('page')) - 1) * 10
        count_to_fetch = int(request.GET.get('limit'))
        if start_time == '':
            communities = Community.objects.filter(title__icontains=request.GET.get('name'),
                                                   topic__icontains=request.GET.get('introduction')).order_by('id')[
                          start_position:start_position + count_to_fetch]
            res['total'] = Community.objects.filter(title__icontains=request.GET.get('name'),
                                                    topic__icontains=request.GET.get('introduction')).count()
        else:
            communities = Community.objects.filter(title__icontains=request.GET.get('name'),
                                                   topic__icontains=request.GET.get('introduction'),
                                                   create_time__range=(start_time, end_time)).order_by('id')[
                          start_position:start_position + count_to_fetch]
            res['total'] = Community.objects.filter(title__icontains=request.GET.get('name'),
                                                    topic__icontains=request.GET.get('introduction'),
                                                    create_time__range=(start_time, end_time)).count()
        data_item = {"id": 0, "name": "", 'introduction': "", 'add_date': ""}
        for community in communities:
            data_item['id'] = community.id
            data_item['name'] = community.title
            data_item['introduction'] = community.topic
            time = str(community.create_time)
            data_item['add_date'] = time.split('.')[0]
            res['data'].append(data_item)
            data_item = {"id": 0, "name": "", 'introduction': "", 'add_date': ""}
        res["code"] = 200
        res["message"] = "success"
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：" + str(e)
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
            tip = Tip(title=data.get('title'),
                      content=data.get('content'),
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


def delete_tip(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tip_id = data.get('tip_id')
            user_id = data.get('user_id')
            tip = Tip.objects.get(id=tip_id)
            community = tip.community
            community_own = OwnedCommunity.objects.get(community=community)
            if tip.user.id == user_id or tip.user.id == community_own.user.id:
                tip.delete()
                res["code"] = 200
                res["message"] = "success"
            else:
                res["code"] = 400
                res["message"] = "fail"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：删除帖子失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def add_support(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        tip = Tip.objects.get(id=request.GET.get('tip_id'))
        tip.support_times += 1
        tip.save()
        res["code"] = 200
        res["message"] = "success"
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：点赞失败" + str(e)
    return JsonResponse(res)


def add_unsupported(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        tip = Tip.objects.get(id=request.GET.get('tip_id'))
        tip.unsupported_times += 1
        tip.save()
        res["code"] = 200
        res["message"] = "success"
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：反对失败" + str(e)
    return JsonResponse(res)


# 获取帖子内容
def get_tipList(request):
    res = {"code": 400, "message": "", "data": None, "title": "", "topic": ""}
    try:
        res['data'] = []
        community = Community.objects.get(id=request.GET.get('id'))
        res['title'] = community.title
        res['topic'] = community.topic
        date_item = {"id": "", "title": "", "author": "", "content": "", "supported": 0, "unsupported": 0,
                     "commentNum": 0, "postTime": "", 'exactPostTime': ""}
        tips = Tip.objects.filter(community=community).order_by('id')
        for tip in tips:
            date_item['id'] = tip.id
            date_item['title'] = tip.title
            date_item['author'] = tip.user.nickname
            date_item['content'] = tip.content
            date_item['supported'] = tip.support_times
            date_item['unsupported'] = tip.unsupported_times
            time = str(tip.create_time)
            time = time.split('.')[0]
            date_item['postTime'] = time.split(' ')[0]
            date_item['exactPostTime'] = time
            date_item['commentNum'] = Comment.objects.filter(tip=tip).count()
            res['data'].append(date_item)
            date_item = {"id": "", "title": "", "author": "", "content": "", "supported": 0, "unsupported": 0,
                         "commentNum": 0, "postTime": "", 'exactPostTime': ""}
        res["code"] = 200
        res["message"] = "success"
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：" + str(e)
    return JsonResponse(res)


# 创建帖子评论
def add_comment(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tip = Tip.objects.get(id=data.get('tip_id'))
            post_user = User.objects.get(id=data.get('user_id'))
            comment = Comment(content=data.get('text'),
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


def delete_comment(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            comment = Comment.objects.get(id=data.get('comment_id'))
            post_user_id = comment.post_user.id
            tip_owner_id = comment.tip.user.id
            community_owner_id = OwnedCommunity.objects.get(community=comment.tip.community).user.id
            if user_id == post_user_id or user_id == tip_owner_id or user_id == community_owner_id:
                comment.delete()
                res["code"] = 200
                res["message"] = "success"
            else:
                res["code"] = 400
                res["message"] = "fail"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：删除评论失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def get_commentList(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        tip_id = request.GET.get('id')
        tip = Tip.objects.get(id=tip_id)
        comments = Comment.objects.filter(tip=tip).order_by('id')
        res['data'] = []
        data_item = {'id': 0, 'userName': "", "text": "", "date": ""}
        for comment in comments:
            data_item['id'] = comment.id
            data_item['userName'] = comment.post_user.nickname
            data_item['text'] = comment.content
            time = str(comment.create_time)
            data_item['date'] = time.split('.')[0]
            res['data'].append(data_item)
            data_item = {'id': 0, 'userName': "", "text": "", "date": ""}
        res["code"] = 200
        res["message"] = "success"
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：获取评论列表失败" + str(e)
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


# 上传图片
def upload(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        pic = request.FILES.get('file')
        upload_path = 'media/'
        save_path = os.path.join(upload_path, pic.name)
        with open(save_path, 'wb') as f:
            for content in pic.chunks():
                f.write(content)
        res["code"] = 200
        res["message"] = "success"
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：上传图片失败" + str(e)
    return JsonResponse(res)
