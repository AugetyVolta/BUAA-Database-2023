from django.db import models


# Create your models here.


# Photo(图片id,图片路径)
class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(verbose_name="图片路径", max_length=100, blank=False)


# 用户表(用户id,用户名,昵称,密码,性别,年龄,头像id)
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="用户名", max_length=50, blank=False)
    nickname = models.CharField(verbose_name="昵称", max_length=30, blank=False)
    password = models.CharField(verbose_name="密码", max_length=30, blank=False)
    gender = models.CharField(verbose_name="性别", max_length=5, blank=True)
    age = models.IntegerField(verbose_name="年龄", blank=True)
    profile_photo = models.ForeignKey(Photo, on_delete=models.PROTECT)


# 书籍表(书籍id,书名,作者,内容介绍,图片id)
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="书名", max_length=50, blank=False)
    author = models.CharField(verbose_name="作者", max_length=50, blank=False)
    description = models.TextField(verbose_name="内容介绍", default="该书暂时没有介绍", blank=True)
    describe_photo = models.ForeignKey(Photo, on_delete=models.PROTECT)


# 书评(书评id,内容,创建时间,点赞数,反对数)
class BookComment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name="内容", blank=False)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    support_times = models.IntegerField(verbose_name="点赞数", default=0)
    unsupported_times = models.IntegerField(verbose_name="反对数", default=0)


# TODO:书籍书评对应表


class Community(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(verbose_name="主题", max_length=100, blank=False)

