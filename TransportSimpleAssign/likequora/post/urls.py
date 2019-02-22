
from django.urls import path, include, re_path
from .views import home, questionCreate, \
    detailedQuestion, answerLike, user_answers, user_questions, questionDelete, answerDelete

app_name = 'post'

urlpatterns = [
    path('', home, name='home'),
    path('question/create/', questionCreate, name='question-create'),
    path('question/<int:id>/', detailedQuestion, name='question-detail'),
    path('question/<int:id>/delete/', questionDelete, name='question-delete'),
    path('question/<int:q>/answer/<int:a>/like/', answerLike, name='answer-like'),
    path('answer/<int:id>/delete/', answerDelete, name='answer-delete'),
    path('questions/user/', user_questions, name='user-questions'),
    path('answers/user/', user_answers, name='user-answers'),
]