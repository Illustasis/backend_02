import collections

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from System.models import *


@csrf_exempt
def delete(request):
    if request.method == 'POST':
        table = request.POST.get('table')  # 注意所有表名都要大写开头
        id = request.POST.get('id')
        type = request.POST.get('type')

        if table == 'User':
            user = User.objects.get(user_id=id)
            user.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        elif table == 'Book':
            book = Book.objects.get(book_id=id)
            book.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        elif table == 'Movie':
            movie = Movie.objects.get(movie_id=id)
            movie.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        elif table == 'Tele':
            tele = Tele.objects.get(tele_id=id)
            tele.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        elif table == 'Group':
            group = Group.objects.get(group_id=id)
            group.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        elif table == 'Topic':
            topic = Topic.objects.get(topic_id=id)
            topic.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        elif table == 'Score':
            score = Score.objects.get(score_id=id)
            score.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        elif table == 'Article':
            article = Article.objects.get(article_id=id)
            article.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        elif table == 'Collect':
            collect = Collect.objects.filter(user_id=id)  # 删除一个用户的全部收藏(单个的收藏已经有接口进行开关了)
            for c in collect:
                c.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        elif table == 'Like' and type == '1':
            like = Like.objects.get(user_id=id)  # 删除用户的喜欢数
            like.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})
        elif table == 'Like' and type == '21':
            like = Like.objects.filter(resource_id=id).filter(column=1)  # 删除article的喜欢数
            for l in like:
                l.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})
        elif table == 'Like' and type == '22':
            like = Like.objects.filter(resource_id=id).filter(column=2)  # 删除reply的喜欢数
            for l in like:
                l.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        elif table == 'Reply':
            reply = Reply.objects.get(reply_id=id)
            reply.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        elif table == 'Photos':
            photo = Photos.objects.filter(resource_id=id).filter(column=type)  # 删除对应资源id的所有图片,type指向资源类型
            for p in photo:
                p.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        elif table == 'Report':
            report = Report.objects.get(report_id=id)
            report.delete()
            return JsonResponse({'errno': 0, 'msg': '删除成功'})

        else:
            return JsonResponse({'errno': 1000, 'msg': '删除失败，检查输入是否有误'})


# 全部删除
@csrf_exempt
def delete_all(request):
    if request.method == 'POST':
        table = request.POST.get('table')  # 注意所有表名都要大写开头

        if table == 'User':
            user = User.objects.all()
            for u in user:
                u.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'Book':
            book = Book.objects.all()
            for b in book:
                b.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'Movie':
            movie = Movie.objects.all()
            for m in movie:
                m.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'Tele':
            tele = Tele.objects.all()
            for t in tele:
                t.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'Group':
            group = Group.objects.all()
            for g in group:
                g.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'Topic':
            topic = Topic.objects.all()
            for t in topic:
                t.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'Score':
            score = Score.objects.all()
            for s in score:
                s.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'Article':
            article = Article.objects.all()
            for a in article:
                a.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'Collect':
            collect = Collect.objects.all()
            for c in collect:
                c.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'Like':
            like = Like.objects.all()
            for l in like:
                l.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'Reply':
            reply = Reply.objects.all()
            for r in reply:
                r.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'Photos':
            photo = Photos.objects.all()
            for p in photo:
                p.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'Report':
            report = Report.objects.all()
            for r in report:
                r.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        elif table == 'GroupArticle':
            group_article = GroupArticle.objects.all()
            for g in group_article:
                g.delete()
            return JsonResponse({'errno': 0, 'msg': '全部删除成功'})

        else:
            return JsonResponse({'errno': 1000, 'msg': '删除失败，检查输入是否有误'})