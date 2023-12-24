import json
import os

import pandas as pd
from django.db.models import Avg
from django.http import JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib.pyplot as plt

from backend.DigBooks import dig_books
from backend.models import Book, Community, User, Favourite, Score, BookComment, UserBookRelation, Tip, Label, \
    BookLabelRelation, OwnedCommunity, Comment, UserLog


def log(user, content):
    newLog = UserLog(user=user, content=content)
    newLog.save()


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
            log(user, "register")
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
        print('-------------------check_user-------------------')
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
                             'gender': user['gender'], 'age': user['age'], "privilege": user['privilege']}
                response_data = {"user_data": user_data, "token": user_data}
                res["data"] = response_data
                print('-------------------user_login-------------------')
                user = User.objects.get(account=data.get('account'))
                log(user, "login")
            else:
                res['message'] = "密码输入错误"
        else:
            res["message"] = "用户不存在"
    except Exception as e:
        res["message"] = "服务器错误，错误原因：" + str(e)
        res["code"] = 500
    return JsonResponse(res)


def get_userList(request):
    res = {"code": 400, "message": "", "data": None, "total": 0}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            start_position = (int(data.get('page')) - 1) * 10
            count_to_fetch = int(data.get('limit'))
            res['data'] = []
            date_item = {"id": "", "account": "", "nickname": "", "privilege": 3}
            if data.get('id'):
                res['total'] = User.objects.filter(id=data.get('id'), account__icontains=data.get('account'),
                                                   nickname__icontains=data.get('nickname')).count()
                users = User.objects.filter(id=data.get('id'), account__icontains=data.get('account'),
                                            nickname__icontains=data.get('nickname')).order_by('id')[
                        start_position:start_position + count_to_fetch]
            else:
                res['total'] = User.objects.filter(account__icontains=data.get('account'),
                                                   nickname__icontains=data.get('nickname')).count()
                users = User.objects.filter(account__icontains=data.get('account'),
                                            nickname__icontains=data.get('nickname')).order_by('id')[
                        start_position:start_position + count_to_fetch]
            for user in users:
                date_item['id'] = user.id
                date_item['account'] = user.account
                date_item['nickname'] = user.nickname
                date_item['privilege'] = user.privilege
                res['data'].append(date_item)
                date_item = {"id": "", "account": "", "nickname": "", "privilege": 3}
            print('-------------------get_userList-------------------')
            res["code"] = 200
            res["message"] = "success"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def get_userLogList(request):
    res = {"code": 400, "message": "", "data": None, "total": 0}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            start_time = data.get('startTime')
            end_time = data.get('endTime')
            start_position = (int(data.get('page')) - 1) * 10
            count_to_fetch = int(data.get('limit'))
            res['data'] = []
            date_item = {"logId": 0, "id": 0, "account": "", "time": "", "log": ""}
            if data.get('id'):
                user = User.objects.get(id=data.get('id'))
                if start_time != '':
                    logs = UserLog.objects.filter(user=user, create_time__range=(start_time, end_time)).order_by('id')[
                           start_position:start_position + count_to_fetch]
                    res['total'] = UserLog.objects.filter(user=user, create_time__range=(start_time, end_time)).count()
                else:
                    logs = UserLog.objects.filter(user=user).order_by('id')[
                           start_position:start_position + count_to_fetch]
                    res['total'] = UserLog.objects.filter(user=user).count()
            elif data.get('account'):
                user = User.objects.get(account__icontains=data.get('account'))
                if start_time != '':
                    logs = UserLog.objects.filter(user=user, create_time__range=(start_time, end_time)).order_by('id')[
                           start_position:start_position + count_to_fetch]
                    res['total'] = UserLog.objects.filter(user=user, create_time__range=(start_time, end_time)).count()
                else:
                    logs = UserLog.objects.filter(user=user).order_by('id')[
                           start_position:start_position + count_to_fetch]
                    res['total'] = UserLog.objects.filter(user=user).count()
            else:
                if start_time != '':
                    logs = UserLog.objects.filter(create_time__range=(start_time, end_time)).order_by('id')[
                           start_position:start_position + count_to_fetch]
                    res['total'] = UserLog.objects.filter(create_time__range=(start_time, end_time)).count()
                else:
                    logs = UserLog.objects.all().order_by('id')[
                           start_position:start_position + count_to_fetch]
                    res['total'] = UserLog.objects.all().count()
            for log in logs:
                date_item['logId'] = log.id
                date_item['id'] = log.user.id
                date_item['account'] = log.user.account
                time = str(log.create_time)
                date_item['time'] = time.split('.')[0]
                date_item['log'] = log.content
                res['data'].append(date_item)
                date_item = {"logId": 0, "id": 0, "account": "", "time": "", "log": ""}
            print('-------------------get_userLogList-------------------')
            res["code"] = 200
            res["message"] = "success"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def downloadUserLog(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            start_time = data.get('startTime')
            end_time = data.get('endTime')
            date_item = {"logId": 0, "id": 0, "account": "", "time": "", "log": ""}
            if data.get('id'):
                user = User.objects.get(id=data.get('id'))
                if start_time != '':
                    logs = UserLog.objects.filter(user=user, create_time__range=(start_time, end_time)).order_by('id')
                    res['total'] = UserLog.objects.filter(user=user, create_time__range=(start_time, end_time)).count()
                else:
                    logs = UserLog.objects.filter(user=user).order_by('id')
                    res['total'] = UserLog.objects.filter(user=user).count()
            elif data.get('account'):
                user = User.objects.get(account__icontains=data.get('account'))
                if start_time != '':
                    logs = UserLog.objects.filter(user=user, create_time__range=(start_time, end_time)).order_by('id')
                    res['total'] = UserLog.objects.filter(user=user, create_time__range=(start_time, end_time)).count()
                else:
                    logs = UserLog.objects.filter(user=user).order_by('id')
                    res['total'] = UserLog.objects.filter(user=user).count()
            else:
                if start_time != '':
                    logs = UserLog.objects.filter(create_time__range=(start_time, end_time)).order_by('id')
                    res['total'] = UserLog.objects.filter(create_time__range=(start_time, end_time)).count()
                else:
                    logs = UserLog.objects.all().order_by('id')
                    res['total'] = UserLog.objects.all().count()
            result = pd.DataFrame()
            for log in logs:
                date_item['logId'] = log.id
                date_item['id'] = log.user.id
                date_item['account'] = log.user.account
                time = str(log.create_time)
                date_item['time'] = time.split('.')[0]
                date_item['log'] = log.content
                cache = pd.DataFrame(
                    {"logId": [date_item['logId']], "user_id": [date_item['id']], "account": [date_item['account']],
                     "time": [date_item['time']],
                     "log": [date_item['log']]})
                date_item = {"logId": 0, "id": 0, "account": "", "time": "", "log": ""}
                result = pd.concat([result, cache])
            print('-------------------downloadUserLog-------------------')
            if data.get('id'):
                filename = 'userLog_' + data.get('id') + '.xlsx'
            elif data.get('account'):
                user = User.objects.get(account__icontains=data.get('account'))
                filename = 'userLog_' + user.id + '.xlsx'
            else:
                filename = 'userLog_all.xlsx'
            result.head()
            result.to_excel(f'media\\{filename}', index=False)
            res['data'] = filename
            res["code"] = 200
            res["message"] = "success"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def modify_userPrivilege(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=data.get('user_id'))
            old = user.privilege
            user.privilege = data.get('privilege')
            user.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------modify_userPrivilege-------------------')
            opUser = User.objects.get(id=data.get('id'))
            user_data = {'account': user.account, "nickname": user.nickname}
            log(opUser, f"change user {user_data} privilege from {old} to {user.privilege}")
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：" + str(e)
    else:
        res["message"] = "请使用POST方法"
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
                log(User.objects.get(account=data["user_account"]),
                    f"change password from {data['old_password']} to {data['new_password']}")
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
            old_data = User.objects.filter(account=data['account']).values().first()
            User.objects.filter(account=data["account"]).update(nickname=data.get('nickname'),
                                                                age=data.get('age'),
                                                                gender=data.get('gender'))
            res_data = User.objects.filter(account=data['account']).values().first()
            res["code"] = 200
            res['message'] = '更新成功'
            res['data'] = res_data
            print('-------------------modify_user-------------------')
            log(User.objects.get(account=data["account"]), f'change userInfo from {old_data} to {res_data}')
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
            user = User.objects.get(id=data.get('user_id'))
            if user.privilege <= 2:
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
                book_data = Book.objects.filter(name=data.get('name'), author=data.get('author')).values().first()
                log(user, f"add book {book_data}")
            else:
                res["code"] = 400
                res["message"] = "fail"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：书籍添加失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def getIdOfBook(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            bookName = data.get('bookName')
            book = Book.objects.filter(name=bookName).first()
            res['data'] = book.id
            res["code"] = 200
            res["message"] = "success"
            print('-------------------getIdOfBook-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误" + str(e)
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
        print('-------------------check_book-------------------')
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误:检查书籍失败" + str(e)
    return JsonResponse(res)


# 挖掘书籍并添加
def dig_book(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=data.get('user_id'))
            if user.privilege <= 2:
                book_data = dig_books()
                books_to_create = [Book(**data) for data in book_data]
                Book.objects.bulk_create(books_to_create)
                res['data'] = len(book_data)
                res["code"] = 200
                res["message"] = "success"
                print('-------------------dig_book-------------------')
                log(user, f"dig book")
            else:
                res["code"] = 400
                res["message"] = "fail"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：书籍爬取失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def upload_book(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=data.get('user_id'))
            if user.privilege <= 2:
                file_path = "media/" + data.get('filename')
                df = pd.read_excel(file_path)
                book_data = df.to_dict(orient='records')
                books_to_create = [Book(**data) for data in book_data]
                Book.objects.bulk_create(books_to_create)
                res['data'] = len(book_data)
                res["code"] = 200
                res["message"] = "success"
                print('-------------------upload_book-------------------')
                log(user, f"upload {res['data']} books")
            else:
                res["code"] = 400
                res["message"] = "fail"
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
            user = User.objects.get(id=data.get('user_id'))
            if user.privilege <= 2:
                # 记录日志
                book_data = Book.objects.filter(name=data.get('title'), author=data.get('author')).values().first()
                log(user, f"delete book {book_data}")
                # 删除书籍
                book.delete()
                res["code"] = 200
                res["message"] = "success"
                print('-------------------delete_book-------------------')
            else:
                res["code"] = 400
                res["message"] = "fail"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：书籍删除失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def edit_book(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=data.get('user_id'))
            if user.privilege <= 2:
                book = Book.objects.get(name=data.get('name'), author=data.get('author'))
                old_data = Book.objects.filter(name=data.get('name'), author=data.get('author')).values().first()
                relations = BookLabelRelation.objects.filter(book=book)
                tags = data.get('tag')
                if len(tags) != 0:
                    # 删除原来的tag
                    for relation in relations:
                        relation.delete()
                    # 设置新tag
                    for tag in tags:
                        label = Label.objects.get(content=tag)
                        newRelation = BookLabelRelation(book=book, label=label)
                        newRelation.save()
                # 设置新introduction和pic_url
                book.description = data.get('introduction') if data.get('introduction') != '' else book.description
                book.pic_url = data.get('pic_url') if data.get('pic_url') != '' else book.pic_url
                book.save()
                res["code"] = 200
                res["message"] = "success"
                print('-------------------edit_book-------------------')
                book_data = Book.objects.filter(name=data.get('name'), author=data.get('author')).values().first()
                log(user, f"edit book from {old_data} to {book_data}")
            else:
                res["code"] = 400
                res["message"] = "fail"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：修改书籍失败" + str(e)
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
        print('-------------------getBookList-------------------')
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
        print('-------------------get_bookDetailList-------------------')
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
        log(user, f"flip through book {book}")
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：" + str(e)
    finally:
        return JsonResponse(res)


def downLoad_books(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        user = User.objects.get(id=request.GET.get('user_id'))
        if user.privilege <= 2:
            books = Book.objects.all().order_by("id")
            res['data'] = []
            data_item = {"id": 0, "title": "", "author": "", "introduction": "", "score": 0.0, "liked_times": 0,
                         "tag": ""}
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
                data_item['score'] = '%.1f' % Score.objects.filter(book=book).aggregate(
                    Avg('score')).get(
                    'score__avg') if Score.objects.filter(book=book) else 0
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
            print('-------------------downLoad_books-------------------')
            log(user, 'download books')
        else:
            res["code"] = 400
            res["message"] = "fail"
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：" + str(e)
    return JsonResponse(res)


def getRecommendedBooks(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            books = Book.objects.all().order_by("id")
            res['data'] = {"bookName": [], "bookScore": []}
            book_data = []
            all_like_times = Favourite.objects.all().count()
            maxScore = -1
            minScore = 9999999999999.0
            data_item = {"id": 0, "title": "", "score": 0.0, "liked_times": 0, "cmp": 0.0}
            for book in books:
                data_item['id'] = book.id
                data_item['title'] = book.name
                data_item['score'] = float('%.1f' % Score.objects.filter(book_id=book.id).aggregate(
                    Avg('score')).get(
                    'score__avg') if Score.objects.filter(book_id=book.id) else 0.0)
                data_item['liked_times'] = Favourite.objects.filter(book=book).count()
                data_item['cmp'] = float(100 * data_item['score'] / 5.0 + 100 * data_item['liked_times'] / (
                        all_like_times + 1))
                if data_item['cmp'] > maxScore:
                    maxScore = data_item['cmp']
                if data_item['cmp'] < minScore:
                    minScore = data_item['cmp']
                book_data.append(data_item)
                data_item = {"id": 0, "title": "", "score": 0.0, "liked_times": 0, "cmp": 0.0}
            book_data = sorted(book_data, key=lambda x: x["cmp"], reverse=True)
            for i in range(10):
                if abs(maxScore - minScore) < 1e-3:
                    score = 100.0
                else:
                    score = '%.1f' % ((book_data[i]["cmp"] - minScore) / (maxScore - minScore) * 100.0)
                res['data']['bookName'].append(book_data[i]['title'])
                res['data']['bookScore'].append(score)
            res["code"] = 200
            res["message"] = "success"
            print('-------------------getRecommendedBooks-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误" + str(e)
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
            book_data = Book.objects.filter(id=data.get('book_id')).values().first()
            log(user, f'collect book {book_data}')
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
            book_data = Book.objects.filter(id=data.get('book_id')).values().first()
            log(user, f'cancel collect book {book_data}')
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
            book_data = Book.objects.filter(id=data.get('book_id')).values().first()
            log(user, f"rate the book {book_data} {data.get('score')}")
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
            book_data = Book.objects.filter(id=data.get('book_id')).values().first()
            log(user,
                f"Review book {book_data} with \"{data.get('reviewContent')}\" and score of {data.get('starRating')}")
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
        print('-------------------check_community-------------------')
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
            user = User.objects.get(id=data.get('user_id'))
            ownedCommunity = OwnedCommunity(user=user,
                                            community=community)
            ownedCommunity.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_community-------------------')
            community_data = {"name": data.get('name'), "introduction": data.get('introduction')}
            log(user, f'create community {community_data}')
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
            community_data = {"name": community.title, "introduction": community.topic}
            user = User.objects.get(id=data.get("user_id"))
            ownedCommunity = OwnedCommunity.objects.filter(user=user, community=community)
            if ownedCommunity or user.privilege <= 2:
                community.delete()
                res["code"] = 200
                res["message"] = "success"
            else:
                res["code"] = 400
                res["message"] = "fail"
            print('-------------------delete_community-------------------')
            log(user, f'delete community {community_data}')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：删除圈子失败" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


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
        print('-------------------get_communityList-------------------')
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
            tip_data = {'title': data.get('title'), "content": data.get('content')}
            community_data = {"name": community.title, "introduction": community.topic}
            log(user, f'post tip {tip_data} in community {community_data}')
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
            user = User.objects.get(id=user_id)
            tip = Tip.objects.get(id=tip_id)
            community = tip.community
            community_own = OwnedCommunity.objects.get(community=community)
            if tip.user.id == user_id or user_id == community_own.user.id or user.privilege <= 2:
                tip.delete()
                res["code"] = 200
                res["message"] = "success"
                print('-------------------delete_tip-------------------')
                tip_data = {'title': tip.title, "content": tip.content}
                community_data = {"name": community.title, "introduction": community.topic}
                log(user, f'delete tip {tip_data} in community {community_data}')
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
        print('-------------------add_support-------------------')
        tip_data = {'title': tip.title, "content": tip.content}
        user = User.objects.get(id=request.GET.get('id'))
        log(user, f"favor tip {tip_data}")
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
        print('-------------------add_unsupported-------------------')
        tip_data = {'title': tip.title, "content": tip.content}
        user = User.objects.get(id=request.GET.get('id'))
        log(user, f"reject tip {tip_data}")
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
        tips = Tip.objects.filter(community=community, state="已通过").order_by('id')
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
        res['data'] = sorted(res['data'], key=lambda x: x["exactPostTime"], reverse=True)
        res["code"] = 200
        res["message"] = "success"
        print('-------------------get_tipList-------------------')
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：" + str(e)
    return JsonResponse(res)


def getTipsByFavor(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        res['data'] = []
        tips = Tip.objects.all().order_by('id')
        data_item = {"rank": 0, "date": "", "nickname": "", "title": "", "favor": 0}
        tmp = []
        for tip in tips:
            time = str(tip.create_time)
            data_item['date'] = time.split(' ')[0]
            data_item['nickname'] = tip.user.nickname
            data_item['title'] = tip.title
            data_item['favor'] = tip.support_times
            tmp.append(data_item)
            data_item = {"rank": 0, "date": "", "nickname": "", "title": "", "favor": 0}
        tmp = sorted(tmp, key=lambda x: x['favor'], reverse=True)
        for i in range(10):
            tmp[i]['rank'] = i + 1
            res['data'].append(tmp[i])
        res["code"] = 200
        res["message"] = "success"
        print('-------------------getTipsByFavor-------------------')
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：" + str(e)
    return JsonResponse(res)


def getTipsByComments(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        res['data'] = []
        tips = Tip.objects.all().order_by('id')
        data_item = {"rank": 0, "date": "", "nickname": "", "title": "", "comments": 0}
        tmp = []
        for tip in tips:
            time = str(tip.create_time)
            data_item['date'] = time.split(' ')[0]
            data_item['nickname'] = tip.user.nickname
            data_item['title'] = tip.title
            data_item['comments'] = Comment.objects.filter(tip=tip).count()
            tmp.append(data_item)
            data_item = {"rank": 0, "date": "", "nickname": "", "title": "", "comments": 0}
        tmp = sorted(tmp, key=lambda x: x['comments'], reverse=True)
        for i in range(10):
            tmp[i]['rank'] = i + 1
            res['data'].append(tmp[i])
        res["code"] = 200
        res["message"] = "success"
        print('-------------------getTipsByComments-------------------')
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：" + str(e)
    return JsonResponse(res)


# 获取任务
def get_task(request):
    res = {"code": 400, "message": "", "data": None, "total": 0}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            start_position = (int(data.get('page')) - 1) * 10
            count_to_fetch = int(data.get('limit'))
            res['data'] = []
            user = User.objects.get(id=data.get('user_id'))
            date_item = {"id": 0, "time": "", "title": "", "applier": "", "content": "", "status": ""}
            communities = OwnedCommunity.objects.filter(user=user).values('community')
            for community in communities:
                community = Community.objects.get(id=community['community'])
                tips = Tip.objects.filter(community=community)
                for tip in tips:
                    time = str(tip.create_time)
                    date_item['id'] = tip.id
                    date_item['time'] = time.split('.')[0]
                    date_item['title'] = tip.title
                    date_item['applier'] = tip.user.nickname
                    date_item['content'] = tip.content
                    date_item['status'] = "待办" if tip.state == '待审核' else "完成"
                    res['data'].append(date_item)
                    date_item = {"id": 0, "time": "", "applier": "", "content": "", "status": ""}
            res['data'] = sorted(res['data'], key=lambda x: (x["status"] == "待办", x["time"]), reverse=True)
            res['total'] = len(res['data'])
            res['data'] = res['data'][start_position:start_position + count_to_fetch]
            res["code"] = 200
            res["message"] = "success"
            print('-------------------get_task-------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def acceptTip(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tip = Tip.objects.get(id=data.get('tip_id'))
            user = User.objects.get(id=data.get('id'))
            if tip.state == '待审核':
                tip.state = "已通过"
                tip.save()
                res["code"] = 200
                res["message"] = "success"
                print('-------------------acceptTip-------------------')
                tip_data = {'title': tip.title, "content": tip.content}
                log(user, f"accept tip {tip_data}")
            else:
                res["code"] = 400
                res["message"] = "success"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def refuseTip(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tip = Tip.objects.get(id=data.get('tip_id'))
            user = User.objects.get(id=data.get('id'))
            if tip.state == '待审核':
                tip.state = "驳回"
                tip.save()
                res["code"] = 200
                res["message"] = "success"
                print('-------------------refuseTip-------------------')
                tip_data = {'title': tip.title, "content": tip.content}
                log(user, f"refuse tip {tip_data}")
            else:
                res["code"] = 400
                res["message"] = "fail"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


def get_tip_status(request):
    res = {"code": 400, "message": "", "data": None, "total": 0}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            start_position = (int(data.get('page')) - 1) * 10
            count_to_fetch = int(data.get('limit'))
            res['data'] = []
            user = User.objects.get(id=data.get('user_id'))
            tips = Tip.objects.filter(user=user)
            date_item = {"time": "", "title": "", "content": "", "status": ""}
            for tip in tips:
                time = str(tip.create_time)
                date_item['time'] = time.split('.')[0]
                date_item['title'] = tip.title
                date_item['content'] = tip.content
                date_item['status'] = tip.state
                res['data'].append(date_item)
                date_item = {"time": "", "title": "", "content": "", "status": ""}
            res['data'] = sorted(res['data'], key=lambda x: x["time"], reverse=True)
            res['total'] = len(res['data'])
            res['data'] = res['data'][start_position:start_position + count_to_fetch]
            res["code"] = 200
            res["message"] = "success"
            print('------------------get_tip_status--------------------')
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：" + str(e)
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
            comment = Comment(content=data.get('text'),
                              post_user=post_user,
                              tip=tip)
            comment.save()
            res["code"] = 200
            res["message"] = "success"
            print('-------------------add_comment-------------------')
            tip_data = {'title': tip.title, "content": tip.content}
            log(post_user, f'review tip {tip_data} with {comment.content}')
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
            user = User.objects.get(id=user_id)
            comment = Comment.objects.get(id=data.get('comment_id'))
            post_user_id = comment.post_user.id
            tip_owner_id = comment.tip.user.id
            community_owner_id = OwnedCommunity.objects.get(community=comment.tip.community).user.id
            if user_id == post_user_id or user_id == tip_owner_id or user_id == community_owner_id or user.privilege <= 2:
                owner = {'account': comment.post_user.account, "nickname": comment.post_user.nickname}
                log(user, f'delete comment {comment.content} of user {owner}')
                comment.delete()
                res["code"] = 200
                res["message"] = "success"
                print('-------------------delete_comment-------------------')
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
    res = {"code": 400, "message": "", "data": None, "title": "", "community_id": 0}
    try:
        tip_id = request.GET.get('id')
        tip = Tip.objects.get(id=tip_id)
        res['community_id'] = tip.community.id
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
        res['data'] = sorted(res['data'], key=lambda x: x["date"], reverse=True)
        res['title'] = tip.title
        res["code"] = 200
        res["message"] = "success"
        print('-------------------get_commentList-------------------')
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
        file = request.FILES.get('file')
        upload_path = 'media/'
        save_path = os.path.join(upload_path, file.name)
        with open(save_path, 'wb') as f:
            for content in file.chunks():
                f.write(content)
        res["code"] = 200
        res["message"] = "success"
        print('-------------------upload-------------------')
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误：上传图片失败" + str(e)
    return JsonResponse(res)


def getAgeDistribution(request):
    res = {"code": 400, "message": "", "data": None}
    try:

        data = [{'value': 0, 'name': "0-20岁"}, {'value': 0, 'name': "20-40岁"}, {'value': 0, 'name': "40-60岁"},
                {'value': 0, 'name': "60-80岁"}, {'value': 0, 'name': "其他"}]
        users = User.objects.all()
        for user in users:
            age = int(user.age)
            if 0 <= age < 20:
                data[0]['value'] += 1
            elif 20 <= age < 40:
                data[1]['value'] += 1
            elif 40 <= age < 60:
                data[2]['value'] += 1
            elif 60 <= age < 80:
                data[3]['value'] += 1
            else:
                data[4]['value'] += 1
        res['data'] = data
        res["code"] = 200
        res["message"] = "success"
        print('-------------------upload-------------------')
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误" + str(e)
    return JsonResponse(res)


def getReport(request):
    res = {"code": 400, "message": "", "data": None}
    try:
        user = User.objects.get(account=request.GET.get('account'))
        collected_books = Favourite.objects.filter(user=user).count()
        commented_books = UserBookRelation.objects.filter(user=user).count()
        created_circles = OwnedCommunity.objects.filter(user=user).count()
        posted_posts = Tip.objects.filter(user=user).count()
        posted_comments = Comment.objects.filter(post_user=user).count()
        start_time = "00:00:00"
        end_time = "06:00:00"
        morning = UserLog.objects.filter(user=user, create_time__time__gte=start_time,
                                         create_time__time__lte=end_time).count()  # 0-6
        start_time = "06:00:00"
        end_time = "12:00:00"
        afternoon = UserLog.objects.filter(user=user, create_time__time__gte=start_time,
                                           create_time__time__lte=end_time).count()  # 6-12
        start_time = "12:00:00"
        end_time = "18:00:00"
        evening = UserLog.objects.filter(user=user, create_time__time__gte=start_time,
                                         create_time__time__lte=end_time).count()  # 12-18
        start_time = "18:00:00"
        end_time = "23:59:59"
        night = UserLog.objects.filter(user=user, create_time__time__gte=start_time,
                                       create_time__time__lte=end_time).count()  # 18-24
        cnt = morning + afternoon + evening + night
        cnt = 1 if cnt == 0 else cnt
        morning = int(100 * morning / cnt)
        afternoon = int(100 * afternoon / cnt)
        evening = int(100 * evening / cnt)
        night = int(100 * night / cnt)
        activity_data = {'Morning': morning, 'Afternoon': afternoon, 'Evening': evening, 'Night': night}
        # 生成统计图
        labels = list(activity_data.keys())
        values = list(activity_data.values())

        fig, ax = plt.subplots()
        ax.bar(labels, values, color='skyblue')
        ax.set_ylabel('ratio')
        ax.set_title('Log Time Range')

        # 将 Matplotlib 图表保存为 PNG 文件
        chart_filename = 'media/tmp.png'
        fig.savefig(chart_filename, format='png', bbox_inches='tight')
        plt.close()  # 关闭 Matplotlib 图表
        # 报告模板
        report_template = """
        亲爱的{},
        这一年里，你收藏了{}本书，评论了{}本书，创立了{}个圈子，发布了{}条帖子，发布了{}条评论。

        下面是你的活动时间分析表：
        """
        # 使用字符串格式化填充数据
        report = report_template.format(user.nickname, collected_books, commented_books, created_circles, posted_posts,
                                        posted_comments)
        font_path = "SimHei.ttf"  # 替换成你的中文 TrueType 字体文件的路径
        pdfmetrics.registerFont(TTFont('SimHei', font_path))
        # 生成 PDF 文件
        pdf_filename = 'media/个人简报.pdf'
        image_path = "media/tmp.png"
        with open(pdf_filename, 'wb') as pdf_file:
            c = canvas.Canvas(pdf_file, pagesize=letter)

            # 设置字体和字体大小
            c.setFont("SimHei", 12)

            # 在 PDF 页面上绘制报告，指定文本框的宽度，实现自动换行
            width, height = letter
            text_object = c.beginText(12, height - 72)
            text_object.setFont("SimHei", 12)
            text_object.setTextOrigin(12, height - 72)

            lines = report.split('\n')
            for line in lines:
                text_object.textLine(line)
            c.drawText(text_object)
            c.drawInlineImage(image_path, 12, height - 450, width=450, height=300)
            c.save()
        res['data'] = '个人简报.pdf'
        res["code"] = 200
        res["message"] = "success"
        print('-------------------upload-------------------')
    except Exception as e:
        res["code"] = 500
        res["message"] = "服务器错误" + str(e)
    return JsonResponse(res)
