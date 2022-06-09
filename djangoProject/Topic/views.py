from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from System.models import *
import json
import random

@csrf_exempt
def hot(request):
    if request.method == 'POST':
        num = request.POST.get('num')
        list=Topic.objects.all().order_by('heat').all()
        hotlist=[]
        i=0
        while i < int(num):
            hotlist.append({
                'name':list[i].name,
                'id':list[i].topic_id
            })
            i=i+1
        return JsonResponse({'errno':0,'msg':'查询热门话题','data':hotlist})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def random(request):
    if request.method == 'POST':
        list=[]
        topics=[]
        list=Topic.objects.all().order_by('?')[:8]
        for topic in list:
            topics.append({'name':topic.name,'id':topic.topic_id})
        return JsonResponse({'errno':0,'msg':'话题广场','data':topics})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
@csrf_exempt
def detail(request):
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        user_id = request.POST.get('user_id')
        topic = Topic.objects.get(topic_id=topic_id)
        collect = Collect.objects.filter(resource_id=topic_id,user_id=user_id,column=4)
        people = Collect.objects.filter(resource_id=topic_id,column=4)
        if collect.exists():
            return JsonResponse(
                {'errno': 0,
                 'data': {
                     'name':topic.name,'id':topic_id,'intro':topic.introduction,'people':len(people)
                     },
                 'collect': 1})
        else:
            return JsonResponse(
                {'errno': 0,
                 'data': {
                     'name': topic.name, 'id': topic_id, 'intro': topic.introduction,
                     'people':0,'passage':0
                 },
                 'collect': 0})
    else:
        return JsonResponse({'errno': 1000})

@csrf_exempt
def collection(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        collect = Collect.objects.filter(user_id=user_id,column=4)
        print(collect)
        collections=[]
        for item in collect:
            topic = Topic.objects.get(topic_id=item.resource_id)
            collections.append({
                'id': topic.topic_id,
                'name':topic.name,
            })
        return JsonResponse({'errno':0, 'data':collections})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def collect(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        topic_id = request.POST.get('topic_id')
        collection = Collect.objects.filter(resource_id=topic_id, column=4, user_id=user_id)
        if collection.exists():
            return JsonResponse({'errno': 0, 'msg': "收藏成功"})
        collecttopic = Collect(resource_id=topic_id, column=4, user_id=user_id)
        collecttopic.save()
        return JsonResponse({'errno':0, 'msg': "收藏成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def uncollect(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        topic_id = request.POST.get('topic_id')
        collection = Collect.objects.filter(resource_id=topic_id, column=4, user_id=user_id)
        if collection.exists():
            for collect in collection:
                collect.delete()
        return JsonResponse({'errno':0, 'msg': "取消收藏"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def dt(request):
    if request.method == 'POST':
        resource_id = request.POST.get('topic_id')
        user_id = request.POST.get('user_id')
        text = request.POST.get('text')
        article = Article(text=text, author_id=user_id, resource_id=resource_id, heat=0, column=4, likes=0)
        article.save()
        return JsonResponse({'errno': 0, 'msg': '发布成功！', 'data': article.pk})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def my_article(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        articles = Article.objects.filter(column=4).filter(author_id=user_id).order_by('-date')
        passage=[]
        for article in articles:
            passage.append({
                'id':article.article_id,
                'text':article.text
            })
        return JsonResponse({'errno':0, 'data':passage})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def hot_article(request):
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        articles = Article.objects.filter(column=4).filter(resource_id=topic_id).order_by('-heat')
        article_list = []
        for article in articles:
            user = User.objects.get(user_id=article.author_id)
            img = ''
            icon = Photos.objects.filter(column=4, resource_id=user.user_id)
            if icon.exists():
                img = Photos.objects.get(column=4, resource_id=user.user_id).url
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
        topic_id = request.POST.get('topic_id')
        articles = Article.objects.filter(column=4).filter(resource_id=topic_id).order_by('-heat')
        article_list = []
        for article in articles:
            user = User.objects.get(user_id=article.author_id)
            img = ''
            icon = Photos.objects.filter(column=4, resource_id=user.user_id)
            if icon.exists():
                img = Photos.objects.get(column=4, resource_id=user.user_id).url
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