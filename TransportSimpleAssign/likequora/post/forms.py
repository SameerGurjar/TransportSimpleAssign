from django import forms
from .models import Question, Answer


class QuestionForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Question")


class AnswerForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Answer")
