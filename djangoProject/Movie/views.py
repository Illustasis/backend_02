from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from System.models import *
import json
# Create your views here.
@csrf_exempt
def hot(request):
    if request.method == 'POST':
        num = request.POST.get('num')
        movielist=Movie.objects.all().order_by('heat').all()
        hotmovielist=[]
        i=0
        while i<int(num):
            hotmovielist.append({
                'name':movielist[i].name,
                'image':movielist[i].image,
                'director':movielist[i].director,
                'id':movielist[i].movie_id
            })
            i=i+1
        return JsonResponse({'errno':0,'msg':'查询热门电影','data':hotmovielist})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def high(request):
    if request.method == 'POST':
        num = request.POST.get('num')
        movielist=Movie.objects.all().order_by('-score').all()
        highmovielist=[]
        i=0
        while i<int(num):
            highmovielist.append({
                'star':movielist[i].score,
                'name':movielist[i].name,
                'image':movielist[i].image,
                'director':movielist[i].director,
                'id':movielist[i].movie_id
            })
            i=i+1
        return JsonResponse({'errno':0,'msg':'查询热门电影','data':highmovielist})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def collect(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        movie_id = request.POST.get('movie_id')
        collect = Collect(resource_id=movie_id, column=2, user_id=user_id)
        collect.save()
        return JsonResponse({'errno':0, 'msg': "收藏成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def uncollect(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        movie_id = request.POST.get('movie_id')
        collection = Collect.objects.filter(resource_id=movie_id, column=2, user_id=user_id)
        if collection.exists() :
            collect=Collect.objects.get(resource_id=movie_id, column=2, user_id=user_id)
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
        collections = Collect.objects.filter(user_id=user_id,column=2)
        collect=[]
        for item in collections:
            movie = Movie.objects.get(movie_id=item.resource_id)
            collect.append({
                'id': movie.movie_id,
                'name':movie.name,
                'info':'[导演]'+movie.director,
                'image':movie.image,
                'star':movie.score,
                'year':movie.year
            })
        return JsonResponse({'errno':0, 'data':collect})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def detail(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')  # 获取图书ID
        user_id = request.POST.get('user_id')  # 获取用户ID
        movie = Movie.objects.get(movie_id=movie_id)
        users_id = Collect.objects.filter(resource_id=movie_id,column=2,user_id=user_id)
        star = Score.objects.filter(column=2, resource_id=movie_id, user_id=user_id)
        myscore = 0.0
        if star.exists():
            star = Score.objects.get(column=2, resource_id=movie_id, user_id=user_id)
            myscore = star.score
        people = Score.objects.filter(column=2, resource_id=movie_id)
        peoplenum = len(people)
        rank_list = []
        i = 1.0
        while i < 6:
            rank_num = len(Score.objects.filter(column=2, resource_id=movie_id, score=i))
            rank_list.append(rank_num)
            i = i + 1.0
        if users_id.exists(): # 查找该用户是否在列表内，在则返回已关注，否则返回未关注
            return JsonResponse(
                {'errno': 0,
                 'data':{
                 'movie_id': movie.movie_id, 'name': movie.name, 'image': movie.image, 'director':movie.director,
                 'actor': movie.actor, 'year':movie.year, 'intro': movie.introduction, 'score': movie.score, 'heat': movie.heat},
                 'collect': 1,'evaluate':myscore,'people':peoplenum,'list':rank_list})
        else:
            return JsonResponse(
                {'errno': 0,
                 'data': {
                     'movie_id': movie.movie_id, 'name': movie.name, 'image': movie.image, 'director': movie.director,
                     'actor': movie.actor, 'year': movie.year, 'intro': movie.introduction, 'score': movie.score,
                     'heat': movie.heat},
                 'collect': 0,'evaluate':myscore,'people':peoplenum,'list':rank_list})

    else:
        return JsonResponse({'errno': 1000})


@csrf_exempt
def commentMovie(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        user_id = request.POST.get('user_id')
        title=request.POST.get('title')
        text=request.POST.get('text')
        article=Article(title=title, text=text, author_id=user_id, resource_id=movie_id, heat=0, column=2, likes=0)
        article.save()
        return JsonResponse({'errno': 0, 'msg': '发布成功！', 'data': article.pk})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def hot_article(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        articles = Article.objects.filter(column=2).filter(resource_id=movie_id).order_by('-heat')
        article_list = []
        for article in articles:
            user = User.objects.get(user_id=article.author_id)
            img = ''
            icon = Photos.objects.filter(column=1, resource_id=user.user_id)
            if icon.exists():
                img = Photos.objects.get(column=1, resource_id=user.user_id).url
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
        movie_id = request.POST.get('movie_id')
        articles = Article.objects.filter(column=2).filter(resource_id=movie_id).order_by('-date')
        article_list = []
        for article in articles:
            user = User.objects.get(user_id=article.author_id)
            img = ''
            icon = Photos.objects.filter(column=1, resource_id=user.user_id)
            if icon.exists():
                img = Photos.objects.get(column=1, resource_id=user.user_id).url
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
def star(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        user_id = request.POST.get('user_id')
        newscore = request.POST.get('score')
        star = Score.objects.filter(column=2,resource_id=movie_id,user_id=user_id)
        if star.exists():
            star = Score.objects.get(column=2,resource_id=movie_id,user_id=user_id)
            star.score=newscore
            star.save()
        else:
            star = Score(user_id=user_id,resource_id=movie_id,column=2,score=newscore)
            star.save()
        scores= Score.objects.filter(column=2,resource_id=movie_id)
        sum=0
        num=0
        for score in scores:
            sum=sum+score.score
            num=num+1
        average = sum/num
        movie = Movie.objects.get(movie_id=movie_id)
        movie.score=average
        movie.save()
        return JsonResponse({'errno':0, 'data':star.score,'msg':'评分成功！'})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def my_article(request):
    if request.method == 'POST':
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            articles = Article.objects.filter(column=2).filter(author_id=user_id).order_by('-date')
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
def hotcomment(request):
    if request.method == 'POST':
        articles = Article.objects.filter(column=2).order_by('-heat')
        # 不确定这里是从早到晚排序还是从晚到早排序，测试时如果遇到相反的可以把order_by后面括号内的'-date'改成'date'
        article_list = []
        for article in articles:
            user_id = article.author_id
            user = User.objects.get(user_id=user_id)
            image = Photos.objects.filter(resource_id=user_id, column=1)
            movie = Movie.objects.get(movie_id=article.resource_id)
            icon = ""
            if image.exists():
                image = Photos.objects.get(resource_id=user_id, column=1)
                icon = image.url
            passage = {
                'username': user.name,
                'usericon': icon,
                'id': article.article_id,
                'moviename': movie.name,
                'movieid': movie.movie_id,
                'img': movie.image,
                'title': article.title,
                'content': article.text,
            }
            article_list.append(passage)
        return JsonResponse({'errno':0, 'data':article_list})
    else:
        return JsonResponse({'errno': 1001, 'msg': '失败，请求方式错误'})