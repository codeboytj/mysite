# coding=utf-8
from django.conf.urls import url
from . import views

# polls应用中的url配置
urlpatterns=[
    # 将符合正则表达式'^$'的url匹配views.py中设置的index视图,polls/
    url(r'^$',views.index,name='index'),
    # 匹配带参数的详情视图,P<question_id>定义了传入view.detail中的匹配的参数名字，polls/5/
    url(r'^(?P<question_id>[0-9]+)/$',views.detail,name='detail'),
    # 匹配投票结果视图,polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$',views.results,name='results'),
    # 匹配投票视图,polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$',views.vote,name='vote'),
]