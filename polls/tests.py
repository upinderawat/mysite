from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently(self):
        # with future question
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_pub_recently(), False)

    def test_was_published_lately(self):
        #with past question
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_pub_recently(), False)

    def test_was_published_currently(self):
        #with todays question
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds= 59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_pub_recently(), True)
