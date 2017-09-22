# coding=utf-8
from rest_framework import serializers
from polls.models import Question,Choice

class QuestionSerializer(serializers.ModelSerializer):

    # 使用ModelSerializer的方式序列化，它会有一个默认的create()和update()方法的实现
    class Meta:
        # 定义需要序列化的模型
        model=Question
        # 定义需要序列化的field
        fields=('id','question_text','pub_date')

class ChoiceSerializer(serializers.ModelSerializer):

    # 使用ModelSerializer的方式序列化，它会有一个默认的create()和update()方法的实现
    class Meta:
        # 定义需要序列化的模型
        model=Choice
        # 定义需要序列化的field
        fields=('id','choice_text','votes')

# 详情页面
class QuestionDetailSerializer(serializers.ModelSerializer):

    # Question的Model中并没有定义choice字段，需要在这儿定义一个自定义的choice字段
    choice=serializers.SerializerMethodField()

    # 定义choice获取的详细方法
    def get_choice(self,obj):
        choices=Choice.objects.filter(question=obj)
        return ChoiceSerializer(choices,many=True,read_only=True).data

    # 使用ModelSerializer的方式序列化，它会有一个默认的create()和update()方法的实现
    class Meta:
        # 定义需要序列化的模型
        model=Question
        # 定义需要序列化的field
        fields=('id','question_text','pub_date','choice')
