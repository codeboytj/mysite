# coding=utf-8
from django.db import models

# Create your models here.

# 模型（M），对应数据库里面的表
class Question(models.Model):
    # 模型的属性，对应数据库表格里面的字段
    # 问题内容
    question_text=models.CharField(max_length=200)
    # 发布时间
    pub_date=models.DateTimeField('date published')

class Choice(models.Model):
    question=models.ForeignKey(Question)
    # 关于question的一个选择的内容
    choice_text=models.CharField(max_length=200)
    # 该选择的得票
    votes=models.IntegerField(default=0)
