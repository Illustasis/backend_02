from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from System.models import *
import json

@csrf_exempt
def bookcomment(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article=Article.objects.get(article_id=article_id)
        print(Article.objects.all().values('article_id','author_id'))
        book=Book.objects.get(book_id=article.resource_id)
        user=User.objects.get(user_id=article.author_id)
        score=Score.objects.get(column=1,resource_id=article.resource_id,user_id=article.author_id)
        like = Collect.objects.filter(column=1,resource_id=article_id)
        reply = Reply.objects.filter(article_id=article_id)
        icon = Photos.objects.filter(resource_id=user.user_id,column=1)
        if icon.exists():
            icon = Photos.objects.get(resource_id=user.user_id,column=1).url
        else:
            icon = ""
        content={
            'username':user.name,
            'icon':icon,
            'user_id':user.user_id,
            'title':article.title,
            'content':article.text,
            'date':article.date,
            'star':score.score,
            'like':len(like),
            'reply':len(reply)
        }
        resource={
            'name':book.name,
            'id':book.book_id,
            'star':book.score,
            'img':book.image,
            'writer':book.author,
        }
        return JsonResponse({'errno':0,'msg':'查询书评详情','data':{'passage':content,'resource':resource}})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def dt(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article=Article.objects.get(article_id=article_id)
        topic = Topic.objects.get(topic_id=article.resource_id)
        user=User.objects.get(user_id=article.author_id)
        collect = Collect.objects.filter(column=4,resource_id=topic.topic_id)
        like = Collect.objects.filter(column=1, resource_id=article_id)
        dtNum = Article.objects.filter(column=4,resource_id=topic.topic_id)
        reply = Reply.objects.filter(article_id=article_id)
        icon = Photos.objects.filter(resource_id=user.user_id, column=1)
        if icon.exists():
            icon = Photos.objects.get(resource_id=user.user_id, column=1).url
        else:
            icon = ""
        content={
            'username':user.name,
            'icon':icon,
            'user_id':user.user_id,
            'content':article.text,
            'date':article.date,
            'like':len(like),
            'reply':len(reply)
        }
        resource={
            'name':topic.name,
            'id':topic.topic_id,
            'collect':len(collect),
            'num':len(dtNum),
        }
        return JsonResponse({'errno':0,'msg':'查询书评详情','data':{'passage':content,'resource':resource}})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def moviecomment(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article=Article.objects.get(article_id=article_id)
        print(Article.objects.all().values('article_id','author_id'))
        movie=Movie.objects.get(movie_id=article.resource_id)
        user=User.objects.get(user_id=article.author_id)
        score=Score.objects.get(column=2,resource_id=article.resource_id,user_id=article.author_id)
        like = Collect.objects.filter(column=1,resource_id=article_id)
        reply = Reply.objects.filter(article_id=article_id)
        icon = Photos.objects.filter(resource_id=user.user_id,column=1)
        if icon.exists():
            icon = Photos.objects.get(resource_id=user.user_id,column=1).url
        else:
            icon = ""
        content={
            'username':user.name,
            'icon':icon,
            'user_id':user.user_id,
            'title':article.title,
            'content':article.text,
            'date':article.date,
            'star':score.score,
            'like':len(like),
            'reply':len(reply)
        }
        resource={
            'name':movie.name,
            'id':movie.movie_id,
            'star':movie.score,
            'img':movie.image,
            'director':movie.director,
        }
        return JsonResponse({'errno':0,'msg':'查询书评详情','data':{'passage':content,'resource':resource}})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def telecomment(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article=Article.objects.get(article_id=article_id)
        print(Article.objects.all().values('article_id','author_id'))
        tele=Tele.objects.get(tele_id=article.resource_id)
        user=User.objects.get(user_id=article.author_id)
        score=Score.objects.get(column=3,resource_id=article.resource_id,user_id=article.author_id)
        like = Collect.objects.filter(column=1,resource_id=article_id)
        reply = Reply.objects.filter(article_id=article_id)
        icon = Photos.objects.filter(resource_id=user.user_id,column=1)
        if icon.exists():
            icon = Photos.objects.get(resource_id=user.user_id,column=1).url
        else:
            icon = ""
        content={
            'username':user.name,
            'icon':icon,
            'user_id':user.user_id,
            'title':article.title,
            'content':article.text,
            'date':article.date,
            'star':score.score,
            'like':len(like),
            'reply':len(reply)
        }
        resource={
            'name':tele.name,
            'id':tele.tele_id,
            'nation': tele.nation,
            'img':tele.image,
            'year':tele.year
        }
        return JsonResponse({'errno':0,'msg':'查询影评详情','data':{'passage':content,'resource':resource}})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})