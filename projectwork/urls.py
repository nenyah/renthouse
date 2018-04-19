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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth.views import logout
from django.conf import settings
from workapp.views import alteruser, appointment, detail, index, list, login_view, register, userinfo, forgetpass, test
from workapp.api import area, house, onehouse

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^alteruser/$', alteruser, name='alteruser'),
    url(r'^appointment/$', appointment, name='appointment'),
    url(r'^detail/(?P<id>\d+)/$', detail, name='detail'),
    url(r'^index/$', index, name='index'),
    url(r'^list/$', list, name='list'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout, {'next_page': '/index/'}, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^userinfo/$', userinfo, name='userinfo'),
    url(r'^forgetpass/$', forgetpass, name='forgetpass'),
    url(r'^api/areas/$', area),
    url(r'^api/houses/$', house),
    url(r'^api/houses/(?P<id>\d+)$', onehouse),
    url(r'^test/$', test),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
