from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from backend.models import Book, Community, User


# Create your views here.
def create_user(request):
    res = {"code": 400, "message": "", "data": None}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = User.objects.create(**data)
            user.save()
            res["code"] = 200
            res["message"] = "success"
        except Exception as e:
            res["code"] = 500
            res["message"] = "服务器错误：" + str(e)
    else:
        res["message"] = "请使用POST方法"
    return JsonResponse(res)


# 用户登录
def log_in(request):
    pass
