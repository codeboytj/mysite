# coding=utf-8
from django.test import TestCase
from django.utils import timezone
import datetime
from django.core.urlresolvers import reverse
from polls.models import Question,Choice

# Create your tests here.

# django会查找TestCase的一个子类
class QuestionMethodTests(TestCase):

    # 测试的方法名字以test开始
    def test_was_published_recently_with_futhure_question(self):
        # 创建一个发布日期为未来的question
        time=timezone.now()+datetime.timedelta(days=30)
        future_question=Question(question_text=u"未来的问题", pub_date=time)
        self.assertEquals(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        # 创建一个发布日期为30天以前的question
        time=timezone.now()-datetime.timedelta(days=30)
        future_question=Question(question_text=u"老旧的问题", pub_date=time)
        self.assertEquals(future_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        # 创建一个发布日期为刚刚的question
        time=timezone.now()-datetime.timedelta(hours=1)
        future_question=Question(question_text=u"刚刚的问题", pub_date=time)
        self.assertEquals(future_question.was_published_recently(),True)


# 快捷创建Question
def create_question(question_text,days):
    time=timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionViewTests(TestCase):
    # 当没有创建任何问题的时候
    def test_index_view_with_no_questions(self):
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    # 当仅仅创建过去的问题的时候
    def test_index_view_with_past_questions(self):
        create_question(question_text="Past question.",days=-30)
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    # 当仅仅创建过去的问题的时候
    def test_index_view_with_future_questions(self):
        create_question(question_text="Future question.",days=30)
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    # 当创建过去以及未来的问题的时候
    def test_index_view_with_past_future_questions(self):
        create_question(question_text="Past question.",days=-30)
        create_question(question_text="Future question.",days=30)
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    # 当创建多个过去问题的时候
    def test_index_view_with_two_past_questions(self):
        create_question(question_text="Past question.",days=-30)
        create_question(question_text="Past question1.",days=-30)
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question1.>','<Question: Past question.>'])

class QuestionIndexDetailTests(TestCase):
    # 如果用户直接通过url访问未来的问题，那么应该直接返回404
    def test_detail_view_with_a_future_question(self):
        future_question=create_question(question_text="Future question.",days=30)
        response=self.client.get(reverse('polls:detail',args=(future_question.id,)))
        self.assertEqual(response.status_code,404)

    # 如果用户直接通过url访问过去的问题，那么正常响应
    def test_detail_view_with_a_past_question(self):
        past_question=create_question(question_text="Past question.",days=-30)
        response=self.client.get(reverse('polls:detail',args=(past_question.id,)))
        self.assertEqual(response.status_code,200)
