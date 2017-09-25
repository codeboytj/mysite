# coding=utf-8
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.template import RequestContext,loader
from django.core.urlresolvers import reverse
# 引入django的通用视图
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Question,Choice
from .serializers import QuestionSerializer,QuestionDetailSerializer,VoteDetailSerializer

# Create your views here.

# rest风格返回问题列表
def question_list(request):

    if request.method=='GET':
        questions=Question.objects.all()
        serializer=QuestionSerializer(questions,many=True)
        return JsonResponse(serializer.data,safe=False)

# rest风格返回问题详情列表
def question_detail(request,pk):

    try:
        question=Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return HttpResponse(status=404)

    if request.method=='GET':
        serializer=QuestionDetailSerializer(question)
        return JsonResponse(serializer.data)

# rest风格的投票视图
# @api_view注解用来使用在函数之前
@api_view(['POST'])
@csrf_exempt
def question_vote(request,question_id):
    # 先找找有没有符合id的question
    p=get_object_or_404(Question,pk=question_id)

    try:
        # 根据post传过来的名为choice的radio标签传过来的id参数，找到相应choice
        # 使用request.data代替request.POST，可以用于多种method，比如PUT,PATCH等
        selected_choice=p.choice_set.get(pk=request.data['choice'])
    except(KeyError,Choice.DoesNotExist):
        # 投票出错，以error_message返回错误信息，显示在detail页面上
        # 返回投票出错的json
        return render(request,'polls/detail.html',{
            'question':p,
            'error_message':"You didn't select a choice"
        })
    else:
        # 得票数自增,通过save方法改动到数据库
        selected_choice.votes+=1;
        selected_choice.save()
        # 返回投票成功的json
        # 不传入many=True，因为现在传入的Question只有一个对象，不然要报错
        serializer=VoteDetailSerializer(p)
        # 使用这个status.HTTP_201_CREATED，使用post请求时居然生成了一个像文档的接口页面
        return Response(serializer.data,status=status.HTTP_201_CREATED)

# 改良视图
class IndexView(generic.ListView):

    template_name='polls/index.html'
    # 传入传页面中的对象列表的参数名
    # 然后generic.ListView会自动使用question_list，所以需要使用context_object_name进行更改以与页面进行匹配
    context_object_name='latest_question_list'

    def get_queryset(self):
        # 修复bug，过滤掉未来的问题
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# 接受参数的视图
# 问题详情页面
class DetailView(generic.DetailView):
    # generic.DetailView这个类从url中获得名为'pk'的主键值，所以需要在urls.py中更改question_id为pk
    # 然后generic.DetailView会自动根据Question，生成名为question的模型加入context
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        # 修复bug，如果用户使用url，可以直接进入未来的问题详情页面，进行投票，所以需要将未来的问题进行过滤
        return Question.objects.filter(pub_date__lte=timezone.now())

# 投票结果视图
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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
