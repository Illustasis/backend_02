from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from System.models import *
import json


@csrf_exempt
def hotgroup(request):
    if request.method == 'POST':
        num = request.POST.get('num')
        list = Group.objects.all().order_by('heat').all()
        hotlist = []
        i = 0
        while i < int(num) and i < len(list):
            hotlist.append({
                'name': list[i].name,
                'id': list[i].group_id
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
                'thestyle': ''
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
                'thestyle': ''
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
                articlelist.append({
                    'id': article.article_id,
                    'title': article.title,
                    'text': article.text,
                    'author_id': article.author_id,
                    'date': article.date,
                    'heat': article.heat,
                    'likes': article.likes
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
