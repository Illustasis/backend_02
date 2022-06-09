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
        likes = Like.objects.filter(resource_id=article_id, column=1)
        article.likes = len(likes)
        article.save()
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
            'like':article.likes,
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
        likes = Like.objects.filter(resource_id=article_id, column=1)
        article.likes = len(likes)
        article.save()
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
            'like':article.likes,
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
        likes = Like.objects.filter(resource_id=article_id, column=1)
        article.likes = len(likes)
        article.save()
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
            'like':article.likes,
            'reply':len(reply)
        }
        resource={
            'name':movie.name,
            'id':movie.movie_id,
            'star':movie.score,
            'img':movie.image,
            'year':movie.year,
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
        tele=Tele.objects.get(tele_id=article.resource_id)
        user=User.objects.get(user_id=article.author_id)
        score=Score.objects.get(column=3,resource_id=article.resource_id,user_id=article.author_id)
        likes = Like.objects.filter(resource_id=article_id, column=1)
        article.likes = len(likes)
        article.save()
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
            'like':article.likes,
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

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article=Article.objects.filter(article_id=article_id)
        if article.exists():
            article = Article.objects.get(article_id=article_id)
            article.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})
        else:
            return JsonResponse({'errno': 100, 'msg': '文章不存在'})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def iflike(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        article_id = request.POST.get('article_id')
        like = Like.objects.filter(resource_id=article_id, column=1, user_id=user_id)
        if like.exists():
            return JsonResponse({'errno': 0, 'data':1})
        else:
            return JsonResponse({'errno': 0, 'data':0})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def like(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        article_id = request.POST.get('article_id')
        like = Like.objects.filter(resource_id=article_id, column=1, user_id=user_id)
        if like.exists():
            return JsonResponse({'errno': 0, 'msg': "点赞过了"})
        like = Like(resource_id=article_id, column=1, user_id=user_id)
        like.save()
        return JsonResponse({'errno':0, 'msg': "点赞成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def unlike(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        article_id = request.POST.get('article_id')
        like = Like.objects.filter(resource_id=article_id, column=1, user_id=user_id)
        if like.exists():
            like.delete()
            article = Article.objects.filter(article_id=article_id)
            if article.exists():
                article = Article.objects.get(article_id=article_id)
                likes = Like.objects.filter(resource_id=article_id, column=1)
                article.likes = len(likes)
                article.save()
            return JsonResponse({'errno': 0, 'msg': "取消点赞"})
        return JsonResponse({'errno':0, 'msg': "点赞成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def like(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        article_id = request.POST.get('article_id')
        like = Like.objects.filter(resource_id=article_id, column=1, user_id=user_id)
        if like.exists():
            return JsonResponse({'errno': 0, 'msg': "点赞过了"})
        like = Like(resource_id=article_id, column=1, user_id=user_id)
        like.save()
        return JsonResponse({'errno':0, 'msg': "点赞成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})