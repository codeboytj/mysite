# coding=utf-8
import datetime

from django.db import models
from django.utils import timezone
from jsonfield import JSONField
# from django.utils.datetime_safe import datetime

# Create your models here.

# 模型（M），对应数据库里面的表


class Question(models.Model):
    # 模型的属性，对应数据库表格里面的字段
    # 问题内容
    question_text=models.CharField(max_length=200)
    # 发布时间
    pub_date=models.DateTimeField('date published')
    # 其他信息，使用Json字符串，便于扩展
    extra=JSONField()

    # 是否近期发布
    def was_published_recently(self):
        now=timezone.now()
        # 修复Bug，对于未来发布的返回false
        return now-datetime.timedelta(days=1)<=self.pub_date<=now

    # 这句话效果是：当管理页面点击was_published_recently进行排序的时候，管理页面按照pub_date字段进行排序
    was_published_recently.admin_order_field='pub_date'
    # 没搞懂这代码是干啥的呢？
    was_published_recently.boolean=True
    # 初始的时候管理页面的该列标题为'was_published_recently'，这样设置之后就变成了'Published recently'
    was_published_recently.short_description='Published recently'

    # 对于python2，定义__unicode__()方法方便命令行操作，django有一个默认的__str__()方法，
    # 它会调用__unicode__()并将结果转换为utf8字符串。对于python3,应该直接定义__str__()方法。
    # 在命令行使用Question()传入中文的时候，要加入u，否则命令行出现Bad Unicode data，比如Question(question_text=u"未来")
    def __unicode__(self):
        return self.question_text

class Choice(models.Model):
    question=models.ForeignKey(Question,related_name='choices')
    # 关于question的一个选择的内容
    choice_text=models.CharField(max_length=200)
    # 该选择的得票
    votes=models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text
