"""novel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from view import index

urlpatterns = [
    # 正则匹配路径
    # url(r'^$', index.main),
    # url(r'^chapter/(?P<novel_id>[1-9]\d*)/$', index.chapter)
    path('admin/', admin.site.urls),
    path('', index.main),
    path('chapter/<int:novel_id>/', index.chapter)
]
