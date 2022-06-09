from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Photo.views import get_avatar
from System.models import *
import json

@csrf_exempt
def bookcomment(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article=Article.objects.get(article_id=article_id)
        article.heat = article.heat + 1
        article.save()
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
        article.heat = article.heat + 1
        article.save()
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
        article.heat = article.heat + 1
        article.save()
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
        article.heat = article.heat + 1
        article.save()
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
            'star': tele.score,
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
        likes = Like.objects.filter(resource_id=article_id, column=1).values('user_id')
        print(likes)
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

# 发表回复（对文章或对另一个回复）
@csrf_exempt
def reply(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        author_id = request.POST.get('author_id')
        text = request.POST.get('text')
        reply_to = request.POST.get('reply_to')
        if reply_to == 0:
            level1_reply = 0    # 一级评论
        else:
            parent_reply = Reply.objects.get(reply_id=reply_to)
            if parent_reply.reply_to == 0:  # 二级评论
                level1_reply = parent_reply.reply_id
            else:  # 二级评论的子评论
                level1_reply = parent_reply.level1_reply  # 归为一级评论的子评论
        Reply.objects.create(article_id=article_id, author_id=author_id, text=text, reply_to=reply_to, level1_reply=level1_reply)
        return JsonResponse({'errno': 0, 'msg': "回复成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 文章页面获取所有对该文章的回复
@csrf_exempt
def get_reply(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        data = []
        level1_replylist = Reply.objects.filter(article_id=article_id, reply_to=0)      # 一级评论列表
        for e in level1_replylist:
            children = []
            children_replylist = Reply.objects.filter(level1_reply=e.reply_id)     # 该一级评论的子评论
            for f in children_replylist:
                replyed_userid = Reply.objects.get(reply_id=f.reply_to).author_id
                usericon = get_avatar(f.author_id)
                children.append({
                    'reply_id': f.reply_id,
                    'author_id': f.author_id,
                    'author_name': User.objects.get(user_id=f.author_id).name,
                    'usericon': usericon,
                    'text': f.text,
                    'like': f.likes,
                    'replyed_userid': replyed_userid,
                    'replyed_username': User.objects.get(user_id=replyed_userid).name
                })
            usericon = get_avatar(e.author_id)
            data.append({
                'reply_id': e.reply_id,
                'author_id': e.author_id,
                'author_name': User.objects.get(user_id=e.author_id).name,
                'usericon': usericon,
                'text': e.text,
                'like': e.likes,
                'chlidren': children
            })
        return JsonResponse({'errno': 0, 'data': data})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 个人页面获取回复通知
@csrf_exempt
def get_message(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        articles = Article.objects.filter(author_id=user_id)       # 用户发表的文章
        replies = Reply.objects.filter(author_id=user_id)       # 用户发表的回复
        data = []
        for i in articles:
            article_replylist = Reply.objects.filter(article_id=i.article_id)       # 该文章的所有回复
            for j in article_replylist:
                usericon = get_avatar(j.author_id)
                data.append({
                    'author_id': j.author_id,
                    'author_name': User.objects.get(user_id=j.author_id).name,
                    'usericon': usericon,
                     'article_id': i.article_id
                })
        for i in replies:
            reply_replylist = Reply.objects.filter(reply_to=i.reply_id)     # 该回复的所有回复
            for j in reply_replylist:
                usericon = get_avatar(j.author_id)
                data.append({
                    'author_id': j.author_id,
                    'author_name': User.objects.get(user_id=j.author_id).name,
                    'usericon': usericon,
                     'article_id': i.article_id
                })
        return JsonResponse({'errno': 0, 'data': data})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})