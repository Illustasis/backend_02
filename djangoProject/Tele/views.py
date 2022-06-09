from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from System.models import *
import json
# Create your views here.
@csrf_exempt
def hot(request):
    if request.method == 'POST':
        num = request.POST.get('num')
        telelist=Tele.objects.all().order_by('heat').all()
        hottelelist=[]
        i=0
        while i<int(num):
            hottelelist.append({
                'name':telelist[i].name,
                'image':telelist[i].image,
                'year':telelist[i].year,
                'nation':telelist[i].nation,
                'id':telelist[i].tele_id,
            })
            i=i+1
        return JsonResponse({'errno':0,'msg':'查询热门电影','data':hottelelist})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def high(request):
    if request.method == 'POST':
        num = request.POST.get('num')
        telelist=Tele.objects.all().order_by('score').all()
        hightelelist=[]
        i=0
        while i<int(num):
            hightelelist.append({
                'star':telelist[i].score,
                'name':telelist[i].name,
                'image':telelist[i].image,
                'year':telelist[i].year,
                'nation':telelist[i].nation,
                'id':telelist[i].tele_id
            })
            i=i+1
        return JsonResponse({'errno':0,'msg':'查询热门电影','data':hightelelist})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def collect(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        tele_id = request.POST.get('tele_id')
        collect = Collect(resource_id=tele_id, column=3, user_id=user_id)
        collect.save()
        return JsonResponse({'errno':0, 'msg': "收藏成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def uncollect(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        tele_id = request.POST.get('tele_id')
        collection = Collect.objects.filter(resource_id=tele_id, column=3, user_id=user_id)
        if collection.exists() :
            collect=Collect.objects.get(resource_id=tele_id, column=3, user_id=user_id)
            collect.delete()
            return JsonResponse({'errno':0, 'msg': "已取消收藏"})
        else:
            return JsonResponse({'errno':200, 'msg': "取消收藏失败"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def collection(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        collections = Collect.objects.filter(user_id=user_id,column=3)
        collect=[]
        for item in collections:
            tele = Tele.objects.get(tele_id=item.resource_id)
            collect.append({
                'id': tele.tele_id,
                'name':tele.name,
                'year':tele.year,
                'info':'['+tele.nation+']',
                'image':tele.image,
                'star':tele.score,
            })
        return JsonResponse({'errno':0, 'data':collect})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
    

@csrf_exempt
def detail(request):
    if request.method == 'POST':
        tele_id = request.POST.get('tele_id')  # 获取图书ID
        user_id = request.POST.get('user_id')  # 获取用户ID
        tele = Tele.objects.get(tele_id=tele_id)
        users_id = Collect.objects.filter(resource_id=tele_id,column=3,user_id=user_id)# 查询关注此书的用户
        # 生成关注用户ID列表(int数据类型)
        if users_id.exists(): # 查找该用户是否在列表内，在则返回已关注，否则返回未关注
            return JsonResponse(
                {'errno': 0,
                 'data':{
                 'tele_id': tele.tele_id, 'name': tele.name, 'image': tele.image, 'nation':tele.nation,
                 'actor': tele.actor, 'year':tele.year, 'intro': tele.introduction, 'score': tele.score, 'heat': tele.heat},
                 'collect': 1})
        else:
            return JsonResponse(
                {'errno': 0,
                 'data': {
                      'tele_id': tele.tele_id, 'name': tele.name, 'image': tele.image, 'nation':tele.nation,
                       'actor': tele.actor, 'year':tele.year, 'intro': tele.introduction, 'score': tele.score, 'heat': tele.heat},
                 'collect': 0})

    else:
        return JsonResponse({'errno': 1000})


@csrf_exempt
def star(request):
    if request.method == 'POST':
        tele_id = request.POST.get('tele_id')
        user_id = request.POST.get('user_id')
        newscore = request.POST.get('score')
        star = Score.objects.filter(column=3,resource_id=tele_id,user_id=user_id)
        if star.exists():
            star = Score.objects.get(column=3,resource_id=tele_id,user_id=user_id)
            star.score=newscore
            star.save()
        else:
            star = Score(user_id=user_id,resource_id=tele_id,column=3,score=newscore)
            star.save()
        scores= Score.objects.filter(column=3,resource_id=tele_id)
        sum=0
        num=0
        for score in scores:
            sum=sum+score.score
            num=num+1
        average = sum/num
        tele = Tele.objects.get(tele_id=tele_id)
        tele.score=average
        tele.save()
        return JsonResponse({'errno':0, 'data':star.score,'msg':'评分成功！'})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def my_article(request):
    if request.method == 'POST':
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            users = Article.objects.filter(column=3).values('author_id')
            articles = Article.objects.filter(column=3).filter(author_id=user_id).order_by('-date')
            passage = []
            for article in articles:
                passage.append({
                    'id': article.article_id,
                    'title': article.title
                })
            return JsonResponse({'errno': 0, 'data': passage})
        else:
            return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def commentTele(request):
    if request.method == 'POST':
        tele_id = request.POST.get('tele_id')
        user_id = request.POST.get('user_id')
        title=request.POST.get('title')
        text=request.POST.get('text')
        article=Article(title=title, text=text, author_id=user_id, resource_id=tele_id, heat=0, column=3, likes=0)
        article.save()
        return JsonResponse({'errno': 0, 'msg': '发布成功！', 'data': article.pk})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def hot_article(request):
    if request.method == 'POST':
        tele_id = request.POST.get('tele_id')
        articles = Article.objects.filter(column=2).filter(resource_id=tele_id).order_by('-heat')
        article_list = []
        for article in articles:
            user = User.objects.get(user_id=article.author_id)
            img = ''
            icon = Photos.objects.filter(column=3, resource_id=user.user_id)
            if icon.exists():
                img = Photos.objects.get(column=3, resource_id=user.user_id).url
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


@csrf_exempt
def new_article(request):
    if request.method == 'POST':
        tele_id = request.POST.get('tele_id')
        articles = Article.objects.filter(column=3).filter(resource_id=tele_id).order_by('-date')
        article_list = []
        for article in articles:
            user = User.objects.get(user_id=article.author_id)
            img = ''
            icon = Photos.objects.filter(column=3, resource_id=user.user_id)
            if icon.exists():
                img = Photos.objects.get(column=3, resource_id=user.user_id).url
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