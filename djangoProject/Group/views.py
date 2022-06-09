from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from System.models import *
import json


@csrf_exempt
def hotgroup(request):
    if request.method == 'POST':
        num = request.POST.get('num')
        list = Group.objects.all().order_by('-heat').all()
        hotlist = []
        i = 0
        while i < int(num) and i < len(list):
            hotlist.append({
                'name': list[i].name,
                'id': list[i].group_id,
                'member':list[i].member
            })
            i = i + 1
        return JsonResponse({'errno': 0, 'msg': '查询热门小组', 'data': hotlist})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 小组内发布文章
@csrf_exempt
def upload_passage(request):
    if request.method == 'POST':
        resource_id = request.POST.get('group_id')
        user_id = request.POST.get('user_id')
        text = request.POST.get('text')
        title = request.POST.get('title')
        article = Article(title=title, text=text, author_id=user_id, resource_id=resource_id, heat=0, column=5, likes=0)
        article.save()
        return JsonResponse({'errno': 0, 'msg': '发布成功！', 'data': article.pk})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def detail(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')  # 获取图书ID
        group_id = request.POST.get('group_id')  # 获取用户ID
        group = Group.objects.get(group_id=group_id)
        users_id = Collect.objects.filter(resource_id=group_id,column=5,user_id=user_id)# 查询关注此书的用户
        managers = GroupManager.objects.filter(group_id = group_id)
        manager_list = []
        if managers.exists():
            for manager in managers:
                user = User.objects.get(user_id=manager.user_id)
                manager_list.append({
                    'user_id':user.user_id,
                    'name':user.name
                })
        if users_id.exists(): # 查找该用户是否在列表内，在则返回已关注，否则返回未关注
            return JsonResponse(
                {'errno': 0,
                 'data':{
                 'group_id': group.group_id, 'name': group.name, 'image': group.image,
                'member':group.member, 'heat': group.heat,
                 'join': 1,'manager':manager_list}})
        else:
            return JsonResponse(
                {'errno': 0,
                 'data': {
                     'group_id': group.group_id, 'name': group.name, 'image': group.image,
                     'member': group.member, 'heat': group.heat,
                     'join': 0,'manager':manager_list}})

@csrf_exempt
def hot_article(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        articles = Article.objects.filter(column=5).filter(resource_id=group_id).order_by('-heat')
        article_list = []
        for article in articles:
            user = User.objects.get(user_id=article.author_id)
            img = ''
            icon = Photos.objects.filter(column=5, resource_id=user.user_id)
            if icon.exists():
                img = Photos.objects.get(column=5, resource_id=user.user_id).url
            article_list.append({
                'id':article.article_id,
                'username': user.name,
                'userid': user.user_id,
                'date': article.date,
                'content': article.text,
                'title': article.title,
                'usericon': img,
            })
        return JsonResponse({'errno': 0, 'data': article_list})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def new_article(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        articles = Article.objects.filter(column=5).filter(resource_id=group_id).order_by('-date')
        article_list = []
        for article in articles:
            user = User.objects.get(user_id=article.author_id)
            img = ''
            icon = Photos.objects.filter(column=5, resource_id=user.user_id)
            if icon.exists():
                img = Photos.objects.get(column=5, resource_id=user.user_id).url
            article_list.append({
                'id': article.article_id,
                'username': user.name,
                'userid': user.user_id,
                'date': article.date,
                'content': article.text,
                'title': article.title,
                'usericon': img,
            })
        return JsonResponse({'errno': 0, 'data': article_list})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 添加类型(1为置顶，2为加精)
@csrf_exempt
def add_kind(request):
    if request.method == 'POST':
        kind = request.POST.get('kind')
        article_id = request.POST.get('article_id')
        group_id = request.POST.get('group_id')
        article = Article.objects.filter(column=5).filter(resource_id=group_id).filter(article_id=article_id)
        # 搜索小组分类中该小组的同ID文章
        article_in = GroupArticle.objects.filter(article_id=article_id).filter(group_id=group_id).filter(type=kind)
        if article.exists():
            if article_in.exists():
                if kind == '1':
                    return JsonResponse({'errno': 1002, 'msg': '文章已置顶'})
                elif kind == '2':
                    return JsonResponse({'errno': 1003, 'msg': '文章已加精'})
                else:
                    return JsonResponse({'errno': 1004, 'msg': 'kind类型错误'})
            else:
                if kind == '1':
                    a = GroupArticle(article_id=article_id, type=1, group_id=group_id)
                    a.save()
                    return JsonResponse({'errno': 0, 'msg': '文章置顶成功'})
                elif kind == '2':
                    GroupArticle.objects.create(article_id=article_id, type=2, group_id=group_id)
                    return JsonResponse({'errno': 0, 'msg': '文章加精成功'})
                else:
                    return JsonResponse({'errno': 1004, 'msg': 'kind类型错误'})

        else:
            return JsonResponse({'errno': 1000, 'msg': '文章不存在'})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 删除类型(1为置顶，2为加精)
@csrf_exempt
def delete_kind(request):
    if request.method == 'POST':
        kind = request.POST.get('kind')
        article_id = request.POST.get('article_id')
        group_id = request.POST.get('group_id')
        article_in = GroupArticle.objects.filter(article_id=article_id).filter(type=kind).filter(group_id=group_id)
        if article_in:
            article_in.delete()
            if kind == '1':
                return JsonResponse({'errno': 0, 'msg': '取消置顶成功'})
            else:
                return JsonResponse({'errno': 0, 'msg': '取消加精成功'})
        else:
            return JsonResponse({'errno': 1000, 'msg': '对象不存在或者删除类型有误'})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 查找类型(1为置顶，2为加精)
@csrf_exempt
def search_kind(request):
    if request.method == 'POST':
        kind = request.POST.get('kind')
        group_id = request.POST.get('group_id')
        article_in = GroupArticle.objects.filter(type=kind).filter(group_id=group_id)
        if article_in.exists():
            articlelist = []
            for a in article_in:  # 这里我把article的全部属性(除了column和resource_id)都返回了,需要用哪些就保留哪些
                article = Article.objects.get(article_id=a.article_id)
                user = User.objects.get(user_id=article.author_id)
                img = ''
                icon = Photos.objects.filter(column=5, resource_id=user.user_id)
                if icon.exists():
                    img = Photos.objects.get(column=5, resource_id=user.user_id).url
                articlelist.append({
                    'id': article.article_id,
                    'username': user.name,
                    'userid': user.user_id,
                    'date': article.date,
                    'content': article.text,
                    'title': article.title,
                    'usericon': img,
                })
                if kind == '1':
                    return JsonResponse({'errno': 0, 'msg': '查询置顶帖子', 'data': articlelist})
                if kind == '2':
                    return JsonResponse({'errno': 0, 'msg': '查询加精帖子', 'data': articlelist})
        else:
            if kind == '1':
                return JsonResponse({'errno': 1002, 'msg': '无置顶帖子'})
            elif kind == '2':
                return JsonResponse({'errno': 1002, 'msg': '无置顶/加精帖子'})
            else:
                return JsonResponse({'errno': 1004, 'msg': 'kind类型错误'})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def hotpassage(request):
    if request.method == 'POST':
        num = request.POST.get('num')
        articles = Article.objects.filter(column=5).order_by('-heat')
        article_list = []
        i = 0
        for article in articles:
            user = User.objects.get(user_id=article.author_id)
            img = ''
            icon = Photos.objects.filter(column=5, resource_id=user.user_id)
            if icon.exists():
                img = Photos.objects.get(column=5, resource_id=user.user_id).url
            article_list.append({
                'id': article.article_id,
                'username': user.name,
                'userid': user.user_id,
                'date': article.date,
                'title':article.title,
                'content': article.text,
                'usericon': img,
            })
            i = i+1
            if i == num:
                break
        return JsonResponse({'errno': 0, 'data': article_list})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def big(request):
    if request.method == 'POST':
        num = request.POST.get('num')
        list = Group.objects.all().order_by('-member').all()
        biglist = []
        i = 0
        while i < int(num) and i < len(list):
            biglist.append({
                'name': list[i].name,
                'id': list[i].group_id,
                'member': list[i].member,
                'img': list[i].image
            })
            i = i + 1
        return JsonResponse({'errno': 0, 'msg': '查询最多人的小组', 'data': biglist})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def myGroup(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        groups = Collect.objects.filter(column=5,user_id=user_id).values('resource_id')
        group_list = []
        for group_id in groups:
            group = Group.objects.get(group_id = group_id)
            group_list.append(({
                'name': group.name,
                'id':group.group_id,
                'img':group.image,
                'member':group.member
            }))
        return JsonResponse({'errno': 0, 'msg': '查询加入的小组', 'data': group_list})
