from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from System.models import *
import json

@csrf_exempt
def hotbook(request):
    if request.method == 'POST':
        num = request.POST.get('num')
        booklist=Book.objects.all().order_by('-heat').all()
        hotbooklist=[]
        i=0
        while i< int(num):
            hotbooklist.append({
                'name':booklist[i].name,
                'image':booklist[i].image,
                'author':booklist[i].author,
                'id':booklist[i].book_id
            })
            i=i+1
        return JsonResponse({'errno':0,'msg':'查询热门图书','data':hotbooklist})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def highbook(request):
    if request.method == 'POST':
        booklist=Book.objects.all().order_by('-score').all()
        highbooklist=[]
        i=0
        while i<20:
            highbooklist.append({
                'name':booklist[i].name,
                'image':booklist[i].image,
                'star':booklist[i].score,
                'id':booklist[i].book_id
            })
            i=i+1
        return JsonResponse({'errno':0,'msg':'查询热门图书','data':highbooklist})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def collect(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        collectbook = Collect(resource_id=book_id, column=1, user_id=user_id)
        collectbook.save()
        return JsonResponse({'errno':0, 'msg': "收藏成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def uncollect(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        collectbook=Collect.objects.get(resource_id=book_id, column=1, user_id=user_id)
        collectbook.delete()
        return JsonResponse({'errno':200, 'msg': "已取消收藏"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def book_collection(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        collectbook = Collect.objects.filter(user_id=user_id,column=1)
        collections=[]
        for item in collectbook:
            book = Book.objects.get(book_id=item.resource_id)
            collections.append({
                'id': book.book_id,
                'name':book.name,
                'author':book.author,
                'image':book.image,
                'star':book.score,
            })
        return JsonResponse({'errno':0, 'data':collections})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def detail(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')  # 获取图书ID
        user_id = request.POST.get('user_id')  # 获取用户ID
        book = Book.objects.get(book_id=book_id)
        users_id = Collect.objects.filter(resource_id=book_id,column=1,user_id=user_id)# 查询关注此书的用户
        star = Score.objects.filter(column=1, resource_id=book_id,user_id=user_id)
        myscore=0.0
        if star.exists():
            star = Score.objects.get(column=1, resource_id=book_id,user_id=user_id)
            myscore = star.score
        people = Score.objects.filter(column=1, resource_id=book_id)
        peoplenum=len(people)
        rank_list=[]
        i=1.0
        while i<6:
            rank_num = len(Score.objects.filter(column=1, resource_id=book_id,score=i))
            rank_list.append(rank_num)
            i=i+1.0
        # 生成关注用户ID列表(int数据类型)
        if users_id.exists(): # 查找该用户是否在列表内，在则返回已关注，否则返回未关注
            return JsonResponse(
                {'errno': 0,
                 'data':{
                 'book_id': book.book_id, 'name': book.name, 'image': book.image, 'author': book.author,
                 'press': book.press, 'intro': book.introduction, 'score': book.score, 'heat': book.heat},
                 'collect': 1,'evaluate':myscore,'people':peoplenum,'list':rank_list})
        else:
            return JsonResponse(
                {'errno': 0,
                 'data': {
                     'book_id': book.book_id, 'name': book.name, 'image': book.image, 'author': book.author,
                     'press': book.press, 'intro': book.introduction, 'score': book.score, 'heat': book.heat},
                     'collect': 0,'evaluate':myscore,'people':peoplenum,'list':rank_list})

    else:
        return JsonResponse({'errno': 1000})

@csrf_exempt
def star(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        user_id = request.POST.get('user_id')
        newscore = request.POST.get('score')
        star = Score.objects.filter(column=1,resource_id=book_id,user_id=user_id)
        if star.exists():
            star = Score.objects.get(column=1,resource_id=book_id,user_id=user_id)
            star.score=newscore
            star.save()
        else:
            star = Score(user_id=user_id,resource_id=book_id,column=1,score=newscore)
            star.save()
        scores= Score.objects.filter(column=1,resource_id=book_id)
        sum=0
        num=0
        for score in scores:
            sum=sum+score.score
            num=num+1
        average = sum/num
        book = Book.objects.get(book_id=book_id)
        book.score=average
        book.save()
        return JsonResponse({'errno':0, 'data':star.score,'msg':'评分成功！'})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def commentBook(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        user_id = request.POST.get('user_id')
        title=request.POST.get('title')
        text=request.POST.get('text')
        article=Article(title=title,text=text,author_id=user_id,resource_id=book_id,heat=0,column=1,likes=0)
        article.save()
        return JsonResponse({'errno':0,'msg':'发布成功！','data':article.pk})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def hot_article(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        articles = Article.objects.filter(column=1).filter(resource_id=book_id).order_by('-heat')
        article_list = []
        for article in articles:
            user = User.objects.get(user_id=article.author_id)
            img = ''
            icon = Photos.objects.filter(column=1, resource_id=user.user_id)
            if icon.exists():
                img = Photos.objects.get(column=1, resource_id=user.user_id).url
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
        book_id = request.POST.get('book_id')
        articles = Article.objects.filter(column=1).filter(resource_id=book_id).order_by('-date')
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
                'thestyle': ''
            })
        return JsonResponse({'errno': 0, 'data': article_list})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def hotcomment(request):
    if request.method == 'POST':
        articles = Article.objects.filter(column=1).order_by('-heat')
        # 不确定这里是从早到晚排序还是从晚到早排序，测试时如果遇到相反的可以把order_by后面括号内的'-date'改成'date'
        article_list = []
        for article in articles:
            user_id = article.author_id
            user = User.objects.get(user_id=user_id)
            image = Photos.objects.filter(resource_id=user_id, column=1)
            book = Book.objects.get(book_id=article.resource_id)
            icon = ""
            if image.exists():
                image = Photos.objects.get(resource_id=user_id, column=1)
                icon = image.url
            passage = {
                'username': user.name,
                'usericon': icon,
                'id': article.article_id,
                'bookname': book.name,
                'bookid': book.book_id,
                'img': book.image,
                'title': article.title,
                'content': article.text,
                'thestyle':''
            }
            article_list.append(passage)
        return JsonResponse({'errno':0, 'data':article_list})
    else:
        return JsonResponse({'errno': 1001, 'msg': '失败，请求方式错误'})

@csrf_exempt
def my_article(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        articles = Article.objects.filter(column=1).filter(author_id=user_id).order_by('-date')
        passage=[]
        for article in articles:
            passage.append({
                'id':article.article_id,
                'title':article.title
            })
        return JsonResponse({'errno':0, 'data':passage})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

