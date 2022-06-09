import json

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from System.models import *


# 注册
@csrf_exempt
def register(request):  # 继承请求类
    print(request)
    if request.method == 'POST':  # 判断请求方式是否为 POST（此处要求为POST方式）
        username = request.POST.get('username')  # 获取请求体中的请求数据
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if password_1 != password_2:  # 若两次输入的密码不同，则返回错误码errno和描述信息msg
            return JsonResponse({'errno': 1002, 'msg': "两次输入的密码不同"})
        else:
            # 新建 Author 对象，赋值用户名和密码并保存
            new_user = User(name=username, password=password_1)
            new_user.save()  # 一定要save才能保存到数据库中
            return JsonResponse({'errno': 0, 'msg': "注册成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 登录
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')  # 获取请求数据
        password = request.POST.get('password', '')
        user = User.objects.filter(name=username)
        if user.exists():
            author = User.objects.get(name=username)
            if author.password == password:  # 判断请求的密码是否与数据库存储的密码相同
                # 密码正确则将用户名存储于session（django用于存储登录信息的数据库位置）
                request.session['name'] = username
                return JsonResponse({'errno': 0, 'msg': "登录成功", 'data': {'id': author.user_id, 'username': username}})
            else:
                return JsonResponse({'errno': 1002, 'msg': "密码错误"})
        else:
            return JsonResponse({'errno': 1002, 'msg': "用户不存在"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 上传书数据(管理员,先暂时用着)
@csrf_exempt
def savebook(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        image = request.POST.get('img', '')  # 封面图片
        author = request.POST.get('author', '')  # 封面图片
        press = request.POST.get('press', '')  # 封面图片  # 出版社
        introduction = request.POST.get('intro', '')
        book = Book(name=name, image=image, author=author, press=press, introduction=introduction, score=0.0, heat=0)
        book.save()
        savebook = Book.objects.all().values('name', 'book_id')
        print(savebook)
        thisbook = Book.objects.get(name=request.POST.get('name', ''))
        return JsonResponse({'errno': 0, 'msg': "存书成功", 'data': {'id': thisbook.book_id}})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 上传电影数据(管理员,先暂时用着)
@csrf_exempt
def savemovie(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        image = request.POST.get('img', '')  # 封面图片
        director = request.POST.get('director', '')  # 封面图片
        year = request.POST.get('year', '')
        actor = request.POST.get('actor', '')
        introduction = request.POST.get('intro', '')  # 封面图片
        movie = Movie(name=name, image=image, director=director, actor=actor, year=year, introduction=introduction,
                      score=0.0, heat=0)
        movie.save()
        savemovie = Movie.objects.all().values('name', 'movie_id')
        print(savemovie)
        print('\n')
        thismovie = Movie.objects.get(name=request.POST.get('name', ''))
        return JsonResponse({'errno': 0, 'msg': "存电影成功", 'data': {'id': thismovie.movie_id}})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 上传电视剧数据(管理员,先暂时用着)
@csrf_exempt
def savetele(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        image = request.POST.get('img', '')  # 封面图片
        nation = request.POST.get('nation', '')  # 封面图片
        year = request.POST.get('year', '')
        actor = request.POST.get('actor', '')
        introduction = request.POST.get('intro', '')  # 封面图片
        tele = Tele(name=name, image=image, nation=nation, actor=actor, year=year, introduction=introduction, score=0.0,
                    heat=0)
        tele.save()
        savetele = Tele.objects.all().values('name', 'tele_id', 'image')
        print(savetele)
        print('\n')
        thistele = Tele.objects.get(name=request.POST.get('name', ''))
        return JsonResponse({'errno': 0, 'msg': "存电视剧成功", 'data': {'id': thistele.tele_id}})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 上传小组(管理员,先暂时用着)
@csrf_exempt
def savegroup(request):
    if request.method == 'POST':
        thisgroup = Group.objects.filter(name=request.POST.get('name', ''))
        if thisgroup.exists():
            return JsonResponse({'errno': 1000, 'msg': "小组已存在"})
        name = request.POST.get('name', '')
        image = request.POST.get('img', '')  # 封面图片
        group = Group(name=name, heat=0, image=image)
        group.save()
        savegroup = Group.objects.all().values('name', 'group_id')
        print(savegroup)
        thisgroup = Group.objects.get(name=request.POST.get('name', ''))
        return JsonResponse({'errno': 0, 'msg': "存小组成功", 'data': {'id': thisgroup.group_id}})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 上传话题(管理员,先暂时用着)
@csrf_exempt
def savetopic(request):
    if request.method == 'POST':
        thistopic = Topic.objects.filter(name=request.POST.get('name', ''))
        if thistopic.exists():
            return JsonResponse({'errno': 1000, 'msg': "话题已存在"})
        name = request.POST.get('name', '')
        introduction = request.POST.get('intro', '')
        topic = Topic(name=name, introduction=introduction, heat=0)
        topic.save()
        savetopic = Topic.objects.all().values('name', 'topic_id')
        print(savetopic)
        thistopic = Topic.objects.get(name=request.POST.get('name', ''))
        name1 = Topic.objects.get(topic_id=3)
        return JsonResponse({'errno': 0, 'msg': "存话题成功", 'data': {'id': thistopic.topic_id, 'content': name1.name}})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 发起举报
@csrf_exempt
def add_report(request):
    if request.method == 'POST':
        report_title = request.POST.get('report_title')
        report_reason = request.POST.get('report_reason')
        reporter_id = request.POST.get('user_id')
        article_id = request.POST.get('article_id')
        Report.objects.create(report_title=report_title, report_reason=report_reason, reporter_id=reporter_id,
                              article_id=article_id)
        return JsonResponse({'errno': 0, 'msg': "举报成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 管理员查看所有举报
@csrf_exempt
def get_report(request):
    if request.method == 'GET':
        reports = Report.objects.all().values()
        report_list = list(reports)
        return JsonResponse({'errno': 0, 'data': report_list})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
