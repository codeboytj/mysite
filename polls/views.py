# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template import RequestContext,loader
from .models import Question

# Create your views here.

def index(request):
    # 配置index页面视图
    # 获取最新的5个question
    latest_question_list=Question.objects.order_by('-pub_date')[:5]
    # 载入polls/index.html模板
    template=loader.get_template('polls/index.html')
    context=RequestContext(request,{
        'latest_question_list':latest_question_list,
    })
    # 返回给浏览器由模板渲染出来的视图
    return HttpResponse(template.render(context))

# 接受参数的视图
# 问题详情页面
def detail(request,question_id):
    try:
        question=Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        # 没有找打相应的问题返回Http404的视图
        raise Http404("Question does not exist")
    # render的快捷使用方法，传入request，模板的名称，一个字典（相当于之前往context里面传入的字典）
    return render(request,'polls/detail.html',{'question':question})

# 投票结果视图
def results(request,question_id):
    response="You're looking at the result of question %s."
    return HttpResponse(response % question_id)

# 投票视图
def vote(request,question_id):
    response="You're voting on question %s."
    return HttpResponse(response % question_id)
