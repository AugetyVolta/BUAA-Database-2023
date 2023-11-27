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
    # 外键
    profile_photo = models.ForeignKey(Photo, on_delete=models.PROTECT)


# 书籍表(书籍id,书名,作者,内容介绍,图片id)
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="书名", max_length=50, blank=False)
    author = models.CharField(verbose_name="作者", max_length=50, blank=False)
    description = models.TextField(verbose_name="内容介绍", default="该书暂时没有介绍", blank=True)
    # 外键
    describe_photo = models.ForeignKey(Photo, on_delete=models.PROTECT)


# 收藏(收藏id,用户id,被收藏书id)
class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    # 外键
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


# 评分(评分id,评分,用户id,被评价id)
class Score(models.Model):
    id = models.AutoField(primary_key=True)
    score = models.IntegerField(verbose_name="评分", blank=False, default=0)
    # 外键
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


# 书评(书评id,内容,创建时间,点赞数,反对数)
class BookComment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name="内容", blank=False)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    support_times = models.IntegerField(verbose_name="点赞数", default=0)
    unsupported_times = models.IntegerField(verbose_name="反对数", default=0)
    # 外键
    commented_book = models.ForeignKey(Book, on_delete=models.CASCADE)  # 书本被删除时,书评也会被删除


# 书评用户对应表(对应表id,用户id,书评id)
class UserBookRelation(models.Model):
    id = models.AutoField(primary_key=True)
    # 外键
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(BookComment, on_delete=models.CASCADE)


# 圈子(圈子id,主题)
class Community(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.TextField(verbose_name="主题", blank=False)


# 创建圈子表(id,用户id,圈子id)
class CreatedCommunity(models.Model):
    id = models.AutoField(primary_key=True)
    # 外键
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)


# 所属圈子表(id,用户id,圈子id)
class BelongCommunity(models.Model):
    id = models.AutoField(primary_key=True)
    # 外键
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)


# 管理圈子表(id,用户id,圈子id)
class ManageCommunity(models.Model):
    id = models.AutoField(primary_key=True)
    # 外键
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)


# 帖子(帖子id,创建时间,内容,圈子id,创建用户id)
class Tip(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    content = models.TextField(verbose_name="内容", blank=False)
    # 外键
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# 发言(发言id,创建时间,内容,所属帖子id,发言user,回复对象id)
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    content = models.TextField(verbose_name="内容", blank=False)
    # 外键
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE)
    post_user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    replied_user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)


# 标签(标签id,标签内容)
class Label(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(verbose_name="内容", max_length=50, blank=False)


# 书籍标签对应表(id,书籍id,标签id)
class BookLabelRelation(models.Model):
    id = models.AutoField(primary_key=True)
    # 外键
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
