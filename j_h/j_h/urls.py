"""j_h URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from authen.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'home/',HomeView.as_view(),name='home'),
    url(r'^authen/', include(("authen.urls", "authen"), namespace="authen")),
    url(r'^image/',include(("image.urls","image"),namespace="image")),
    url(r'^log/',include(("moment.urls","log"),namespace="log")),
]

#为每个上传的静态图片配置了URL路径
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
