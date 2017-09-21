# coding=utf-8
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext,loader
from django.core.urlresolvers import reverse
from .models import Question,Choice

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

    question=Question.objects.get(pk=question_id)
    return render(request,'polls/results.html',{'question':question})

# 投票视图
def vote(request,question_id):
    # get_object_or_404()为raise Http404的快捷方式，如果有相应的question，则获得相应对象，如果没有则返回404
    p=get_object_or_404(Question,pk=question_id)

    try:
        # 根据post传过来的名为choice的radio标签传过来的id参数，找到相应choice
        selected_choice=p.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        # 投票出错，以error_message返回错误信息，显示在detail页面上
        return render(request,'polls/detail.html',{
            'question':p,
            'error_message':"You didn't select a choice"
        })
    else:
        # 得票数自增,通过save方法改动到数据库
        selected_choice.votes+=1;
        selected_choice.save()
        # 投票成功，返回到投票结果页面
        # reverse()函数使用url中配置的视图名作为参数，避免了使用硬编码，之后设置的args作为参数传给相应的url中的匹配
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
