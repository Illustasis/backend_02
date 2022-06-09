import datetime
import json
from random import Random

import pytz
from django.conf import settings
from django.core import serializers
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from System.models import *


# 生成随机字符串
def random_str():
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(8):
        str += chars[random.randint(0, length)]
    return str


# 获得验证码
@csrf_exempt
def get_code(request):
    print(request)
    if request.method == 'POST':  # 判断请求方式是否为 POST（此处要求为POST方式）
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        email = request.POST.get('email')
        name = request.POST.get('name')
        if Email.objects.filter(email=email).exists():
            status = Email.objects.filter(email=email).first().status
        else:
            status = 0
        if password_1 != password_2:  # 若两次输入的密码不同，则返回错误码errno和描述信息msg
            return JsonResponse({'errno': 1002, 'msg': "两次输入的密码不同"})
        elif status == 1:
            return JsonResponse({'errno': 1002, 'msg': "邮箱已注册"})
        elif User.objects.filter(name=name).exists():
            return JsonResponse({'errno': 1002, 'msg': "用户名已注册"})
        else:
            code = random_str()
            Email.objects.create(code=code, email=email)  # 数据库保存验证码
            email_title = "注册激活"
            email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
            check = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])  # 发送邮件
            if not check:
                return JsonResponse({'errno': 1002, 'msg': "验证码发送失败"})
            else:
                return JsonResponse({'errno': 1000, 'msg': "验证码已发送"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def register(request):
    print(request)
    if request.method == 'POST':
        code = request.POST.get('code')
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        get_by_email = Email.objects.filter(email=email).order_by('-add_time').first()      # 最新验证码记录
        difftime = (datetime.datetime.now(tz=pytz.UTC)-get_by_email.add_time).seconds      # 最新验证码距今多久
        # print(difftime)
        if get_by_email.code != code:
            return JsonResponse({'errno': 1002, 'msg': "验证码错误"})
        elif difftime > 300:
            return JsonResponse({'errno': 1002, 'msg': "验证码已失效"})
        else:
            User.objects.create(name=name, password=password)       # 添加新用户
            # 更新验证码记录表里的状态和用户id属性
            new_user = User.objects.get(name=name)
            Email.objects.filter(email=email).update(status=1, user_id=new_user.user_id)
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
        data = []
        for e in Report.objects.all():
            data.append({
                'reporter_id': e.reporter_id,
                'reporter_name': User.objects.get(user_id=e.reporter_id).name,
                'report_title': e.report_title,
                'report_reason': e.report_reason,
                'result': e.result,
            })
        print(data)
        return JsonResponse({'errno': 0, 'data': data})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
