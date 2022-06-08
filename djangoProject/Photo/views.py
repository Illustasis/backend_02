import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from djangoProject import settings
from Photo.models import *
import datetime

# 上传
@csrf_exempt
def upload_photo(request):
    if request.method == 'POST':
        image = request.FILES.get('photo', '')
        resource_id = request.POST.get('resource_id', '')
        resource_type = request.POST.get('resource_type', '')
        resource = Photos.objects.filter(resource_id=resource_id).filter(column=resource_type)
        image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + request.POST.get('name', '')
        f = open(os.path.join(settings.UPLOAD_FILE, image_name), 'wb')
        for i in image.chunks():
            f.write(i)
        f.close()
        if resource.exists():
            if resource_type == '1':  # 种类是用户头像时
                resource2 = Photos.objects.get(resource_id=resource_id,column=resource_type)
                resource2.url = '/upload/'+image_name
                resource2.save()
                return JsonResponse({'errno':0,'msg':'头像上传成功','data':{'url':'/upload/'+image_name}})
            elif resource_type == '2':  # 种类是文章图片时
                resource3 = Photos.objects.create(url='/upload/'+image_name, resource_id=resource_id, column=resource_type)
                resource3.save()
                return JsonResponse({'errno':0,'msg':'图片上传成功'})
            else:
                return JsonResponse({'errno':100,'msg':'资源种类有限'})
        else:
            if resource_type == '1' or resource_type == '2':
                resource4 = Photos.objects.create(url='/upload/'+image_name, resource_id=resource_id, column=resource_type)
                resource4.save()
                return JsonResponse({'errno':200,'msg':'上传图片成功'})
            else:
                return JsonResponse({'errno':100,'msg':'资源种类有限'})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

# 获取图片
@csrf_exempt
def get_photo(request):
    if request.method == 'POST':
        resource_id = request.POST.get('resource_id', '')
        resource_type = request.POST.get('resource_type', '')
        resource = Photos.objects.filter(resource_id=resource_id).filter(column=resource_type)
        if resource.exists():
            for r in resource:
                return JsonResponse({'errno':0,'photo': r.url})
        else:
            return JsonResponse({'errno':100,'msg':'无图片'})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


