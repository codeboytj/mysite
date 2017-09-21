# coding=utf-8
import datetime

from django.db import models
from django.utils import timezone
# from django.utils.datetime_safe import datetime

# Create your models here.

# 模型（M），对应数据库里面的表


class Question(models.Model):
    # 模型的属性，对应数据库表格里面的字段
    # 问题内容
    question_text=models.CharField(max_length=200)
    # 发布时间
    pub_date=models.DateTimeField('date published')

    # 是否近期发布
    def was_published_recently(self):
        return self.pub_date>=timezone.now() - datetime.timedelta(days=1)

    # 这句话效果是：当管理页面点击was_published_recently进行排序的时候，管理页面按照pub_date字段进行排序
    was_published_recently.admin_order_field='pub_date'
    # 没搞懂这代码是干啥的呢？
    was_published_recently.boolean=True
    # 初始的时候管理页面的该列标题为'was_published_recently'，这样设置之后就变成了'Published recently'
    was_published_recently.short_description='Published recently'

class Choice(models.Model):
    question=models.ForeignKey(Question)
    # 关于question的一个选择的内容
    choice_text=models.CharField(max_length=200)
    # 该选择的得票
    votes=models.IntegerField(default=0)