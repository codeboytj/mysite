# coding=utf-8
from django.contrib import admin
from .models import Choice,Question

# Question的关联对象Choice，
# class ChoiceInline(admin.StackedInline):
# 使用TabularInline代替StackedInline让关联对象的排列变成表格形式的，更加紧凑
class ChoiceInline(admin.TabularInline):
    # 关联的模型
    model = Choice
    # 默认获得3个空白Choice
    extra = 3


# Register your models here.
# 自定义管理表单
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        # 把字段分为多个字段集，也可以通过改变先后顺序来指定html中的字段顺序
        (None,{'fields':['question_text']}),
        # 同时，还可以通过classes指定相应的字段集的html样式
        ('Data Information',{'fields':['pub_date'],'classes':['collapse']}),
    ]
    # 设置关联对象
    inlines = [ChoiceInline]
    # 通过list_display自定义question管理页面中显示的question的字段
    list_display = ('question_text','pub_date','was_published_recently')
    # 过滤器，会出现在question的管理页面中，Djang根据pub_date的类型给出相应选项
    list_filter = ['pub_date']
    # 在管理页面添加按照text搜索question的功能
    search_fields = ['question_text']

admin.site.register(Question,QuestionAdmin)
