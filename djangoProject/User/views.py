from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from System.models import *
import json
# Create your views here.
@csrf_exempt
def detail(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '')
        user = User.objects.filter(user_id=user_id)
        if user.exists():
            user = User.objects.get(user_id=user_id)
            image = Photos.objects.filter(resource_id=user_id, column=1)
            icon = ""
            if image.exists():
                image = Photos.objects.get(resource_id=user_id, column=1)
                icon = image.url
            user.isAdmin = 1
            user.save()
            info = {
                'name': user.name,
                'admin': user.isAdmin,
                'image':icon
            }
            return JsonResponse({'errno': 0, 'msg': '查询到用户信息','data':info})
        else:
            return JsonResponse({'errno': 100, 'msg': '用户不存在'})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
