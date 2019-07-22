from django.shortcuts import render,HttpResponse

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import ImageForm
from .models import Image
from authen.models import UserInfo
from statics.plugins.page.pager import Pagination
from sorl.thumbnail import get_thumbnail
from django.conf import settings
import os

#接收前端处理前端提交的数据
@login_required(login_url='account/login/')
@require_POST  #保证此函数只通过POST方式提交数据
@csrf_exempt
def upload_image(request):
    valid_extensions = ['jpg', 'jpeg', 'png']
    try:
        get_im = request.FILES['im']
        title=request.POST['title']
        im_type = str(get_im).rsplit('.', 1)[1].lower()
        if im_type in valid_extensions:
            if len(get_im) > 3145728:
                return HttpResponse("1")
            else:
                im=Image.objects.create(title=title,user_id=request.user.id,image=get_im)
                im.save()
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    except Exception as e:
        print(e)
        return HttpResponse("4")

#展示图片
@login_required(login_url='account/login/')
def manage_images(request):
    userinfo = UserInfo.objects.get(user=request.user) #用于header中的头像
    images_list=Image.objects.filter(user=request.user)

    c_page = request.GET.get('page')
    page_obj = Pagination(len(images_list), c_page, "/image/manage-images", perPageItemNum=3)
    images = images_list[page_obj.start():page_obj.end()]

    return render(request, 'image/manage_images.html', locals())

#删除图片
@login_required(login_url='account/login/')
@require_POST  #保证此函数只通过POST方式提交数据
@csrf_exempt
def del_image(request):
    image_id=request.POST['image_id']
    try:
        image=Image.objects.get(id=image_id)
        del_path=os.path.join(settings.MEDIA_ROOT,str(image.image))
        os.remove(del_path)
        image.delete()

        return JsonResponse({'status':'1'})
    except Exception:
        return JsonResponse({'status': '2'})

#瀑布流
def falls_images(request):
    if request.user.is_authenticated:
        userinfo = UserInfo.objects.get(user=request.user)  # 用于header中的头像
    images=Image.objects.all()
    return render(request,'image/falls_images.html',locals())

#编辑图片
@login_required(login_url='/account/login/')
def edit_image(request):
    if request.method == "POST":

        image_id=request.POST['image_id']
        im=Image.objects.get(id=image_id)
        im.image=im
        im.save()
        return HttpResponse('1')
    else:
        return render(request,'image/imagecrop.html')

