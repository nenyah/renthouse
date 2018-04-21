"""projectwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth.views import logout
from django.conf import settings
from workapp.views import alteruser, appointment, detail, index, product_list, login_view, register, userinfo, forgetpass, test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alteruser/', alteruser, name='alteruser'),
    path('appointment/', appointment, name='appointment'),
    path('detail/<int:id>/', detail, name='detail'),
    path('index/', index, name='index'),
    path('list/', product_list, name='productlist'),
    # path('list/<int:area>/', product_list, name='product_list'),
    path('login/', login_view, name='login'),
    path('logout/', logout, {'next_page': '/index/'}, name='logout'),
    path('register/', register, name='register'),
    path('userinfo/', userinfo, name='userinfo'),
    path('forgetpass/', forgetpass, name='forgetpass'),
    # path('api/areas/', area),
    # path('api/houses/', house),
    # path('api/houses/<int:id>', onehouse),
    path('test/', test),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
