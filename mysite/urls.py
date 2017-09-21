# coding=utf-8
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # 加入polls中的url配置
    # 需要将127.0.0.1改成localhost，不然的话没有效果
    # 一个项目中可能有多个应用，这时可以使用namespace进行区分，这样需要在使用模板标签{% url %}时，做相应的修改，加上相应的namespace
    url(r'^polls/', include('polls.urls',namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
]
