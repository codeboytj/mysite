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
        fields=('id','choice_text')

# 详情页面
class QuestionDetailSerializer(serializers.ModelSerializer):

    # # 由于question是choice的外键，但是question中没有直接定义choice，所以通过这种方式添加进来
    # # 但是这种方式，需要将model里面的外键约束里面设置，related_name='choices'，不然会提示
    # # XXX has no attribute 'xxx'
    # # 但是这种方法，读出来的Choice只有主键，没有详细的信息，所以还是放弃吧
    # choices=serializers.PrimaryKeyRelatedField(many=True,queryset=Question.objects.all())
    # 另一种方法，Question的Model中并没有定义choice字段，需要在这儿定义一个自定义的choice字段
    # 并通过方法实现返回内容，获得更大的灵活度
    choices=serializers.SerializerMethodField()

    # 定义choice获取的详细方法
    def get_choices(self,obj):
        choices=Choice.objects.filter(question=obj)
        return ChoiceSerializer(choices,many=True,read_only=True).data

    # 使用ModelSerializer的方式序列化，它会有一个默认的create()和update()方法的实现
    class Meta:
        # 定义需要序列化的模型
        model=Question
        # 定义需要序列化的field
        fields=('id','question_text','pub_date','choices')

# 得票页面
class VoteSerializer(serializers.ModelSerializer):

    # 使用ModelSerializer的方式序列化，它会有一个默认的create()和update()方法的实现
    class Meta:
        # 定义需要序列化的模型
        model=Choice
        # 定义需要序列化的field，此时要加上'vote'属性显示每个选项的票数
        fields=('id','choice_text','votes')

# 投票结果页面
class VoteDetailSerializer(serializers.ModelSerializer):

    # Question的Model中并没有定义choice字段，需要在这儿定义一个自定义的choice字段
    choice=serializers.SerializerMethodField()

    # 定义choice获取的详细方法
    def get_choice(self,obj):
        choices=Choice.objects.filter(question=obj)
        return VoteSerializer(choices,many=True,read_only=True).data

    # 使用ModelSerializer的方式序列化，它会有一个默认的create()和update()方法的实现
    class Meta:
        # 定义需要序列化的模型
        model=Question
        # 定义需要序列化的field
        fields=('id','question_text','pub_date','choice')
