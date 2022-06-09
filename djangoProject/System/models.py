from django.db import models


class User(models.Model):
    name = models.CharField(max_length=40)
    isAdmin = models.IntegerField(default=0)
    password = models.CharField(max_length=20)
    user_id = models.AutoField(primary_key=True)


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    image: str = models.CharField(max_length=200)  # 封面图片
    author = models.CharField(max_length=80)
    press = models.CharField(max_length=80)  # 出版社
    introduction = models.TextField(max_length=1000, default='')
    score = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)  # 评分，5分满分，1位小数
    heat = models.IntegerField(default=0)  # 点击量


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    image: str = models.CharField(max_length=200)  # 封面图片
    director = models.CharField(max_length=80)
    actor = models.CharField(max_length=200)
    year = models.IntegerField(default=1990)
    introduction = models.TextField(max_length=1000, default='')
    score = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)  # 评分，5分满分，1位小数
    heat = models.IntegerField(default=0)  # 点击量


class Tele(models.Model):
    tele_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    image: str = models.CharField(max_length=200)  # 封面图片
    nation = models.CharField(max_length=80)
    actor = models.CharField(max_length=200)
    year = models.IntegerField(default=1990)
    introduction = models.TextField(max_length=1000, default='')
    score = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)  # 评分，5分满分，1位小数
    heat = models.IntegerField(default=0)  # 点击量


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    image: str = models.CharField(max_length=200)  # 封面图片
    heat = models.IntegerField(default=0)  # 点击量
    member = models.IntegerField(default=0)  #成员数量

class GroupManager(models.Model):
    group_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)

class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    introduction = models.TextField(max_length=1000, default='')
    heat = models.IntegerField(default=0)  # 点击量


class Score(models.Model):  # 评分表
    score_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    resource_id = models.IntegerField(default=0)  # 相关资源（book,movie)的id
    column = models.IntegerField(default=0)  # 分类 1:book,2:movie,3:tele
    score = models.DecimalField(max_digits=2, decimal_places=1)


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80, null=True)
    text = models.TextField(max_length=10000, default='')
    author_id = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    heat = models.IntegerField(default=0)
    column = models.IntegerField(default=0)  # 分类  1:book,2:movie,3:tele,4:topic,5:group
    resource_id = models.IntegerField(default=0)  # 相关资源（book,movie,topic）的id
    likes = models.IntegerField(default=0)


class Collect(models.Model):
    user_id = models.IntegerField(default=0)
    resource_id = models.IntegerField(default=0)  # 相关资源（book,movie,topic，group）的id
    column = models.IntegerField(default=0)  # 分类 1:book,2:movie,3:tele,4:topic,5:group;


class Like(models.Model):
    user_id = models.IntegerField(default=0)
    resource_id = models.IntegerField(default=0)
    column = models.IntegerField(default=0)  # 分类 1:article,2.reply


class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    article_id = models.IntegerField(default=0)
    text = models.CharField(max_length=80)
    likes = models.IntegerField(default=0)
    author_id = models.IntegerField(default=0)
    reply_to = models.IntegerField(default=0)


class Photos(models.Model):
    url = models.CharField(max_length=200,default='')
    resource_id = models.IntegerField(default=0)  # 带有图片的资源id
    column = models.IntegerField(default=0)  # 用于指向resource_id的分类标志 1:user 2:article ...


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    reporter_id = models.IntegerField(default=0)
    article_id = models.IntegerField(default=0)
    report_title = models.CharField(max_length=80)
    report_reason = models.CharField(max_length=200)
    result = models.IntegerField(default=0)     # 举报结果，0：未处理，1：举报成功，文章已删除，2：失败


class GroupArticle(models.Model):
    group_id = models.IntegerField(default=0)
    article_id = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
