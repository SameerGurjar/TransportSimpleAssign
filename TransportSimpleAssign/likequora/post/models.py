from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
# Create your models here.

User = settings.AUTH_USER_MODEL


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    num_answer = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('post:question-detail', kwargs={'id': self.pk})

    def delete_absolute_url(self):
        return reverse('post:question-delete', kwargs={'id': self.pk})


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.content

    def isAnswered(self):
        status = bool(Answer.objects.get(user=self.user, question=self.question))
        return status

    def get_like_absolute_url(self):
        return reverse('post:answer-like', kwargs={'a': self.pk, 'q': self.question.pk})

    def delete_absolute_url(self):
        return reverse('post:answer-delete', kwargs={'id': self.pk})


class AnswerFavourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)

    def isLiked(self):
        status = bool(AnswerFavourite.objects.get(user=self.user, answer=self.answer))
        return status
