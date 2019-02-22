from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Question, Answer, AnswerFavourite
from .forms import QuestionForm, AnswerForm
from django.db.models import F, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/accounts/login/')
def questionCreate(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            user = request.user
            q = Question.objects.create(content=content, user=user)
            q.save()
            return redirect(reverse('post:home'))
        else:
            context = {
                'form': form
            }
            return render(request, 'post/question_input.html', context)
    else:
        form = QuestionForm()
        context = {
            'form': form
        }
        return render(request, 'post/question_input.html', context)


@login_required(login_url='/accounts/login/')
def questionDelete(request, id):
    question = Question.objects.filter(pk=id, user=request.user)
    deleteed_question = question.first().delete()
    if bool(deleteed_question):
        messages.success(request, 'Question is deleted Successfully')
    else:
        messages.success(request, 'Problem in Deleting Question')
    return redirect(reverse('post:user-questions'))


@login_required(login_url='/accounts/login/')
def user_answers(request):
    answers = Answer.objects.filter(user=request.user)
    context = {
        'answers': answers
    }
    return render(request, 'post/user_answers.html', context)


@login_required(login_url='/accounts/login/')
def answerDelete(request, id):
    answer = Answer.objects.filter(pk=id, user=request.user)
    answer = answer.first()
    deleted_answer = answer.delete()
    if bool(deleted_answer):
        Question.objects.filter(pk=answer.question.pk).update(num_answer=F('num_answer') - 1)
        messages.success(request, 'Answer is deleted Successfully')
    else:
        messages.success(request, 'Problem in Deleting Answer')
    return redirect(reverse('post:user-answers'))


@login_required(login_url='/accounts/login/')
def user_questions(request):
    questions = Question.objects.filter(user=request.user)
    context = {
        'questions': questions
    }
    return render(request, 'post/user_questions.html', context)


def detailedQuestion(request, id):
    question = get_object_or_404(Question, id=id)
    form = AnswerForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(reverse('accounts:login'))
        form = AnswerForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            question = question
            user = request.user
            answer = Answer.objects.filter(user=user, question=question)
            if bool(answer):
                messages.add_message(request, messages.INFO, 'Already Answered')
                return redirect(reverse('post:question-detail', kwargs={'id': id}))
            a = Answer.objects.create(content=content, user=user, question=question)
            a.save()
            Question.objects.filter(pk=id).update(num_answer= F('num_answer') + 1)
            return redirect(reverse('post:question-detail', kwargs={'id': id}))

    answers = Answer.objects.filter(question=question)
    if request.user.is_authenticated:
        for answer in answers:
            answer_fav = AnswerFavourite.objects.filter(answer=answer, user=request.user)
            answer.isliked = False
            if bool(answer_fav):
                answer.isliked = True
    context = {
        'question': question,
        'answers': answers,
        'form': form
    }
    return render(request, 'post/question_detail.html', context)


@login_required(login_url='/accounts/login/')
def answerLike(request, q, a):
    answer = get_object_or_404(Answer, id=a)
    user = request.user

    answer_fav = AnswerFavourite.objects.filter(answer=answer, user=user)
    if bool(answer_fav):
        answer_fav = answer_fav.first()
        answer_fav.delete()
        Answer.objects.filter(pk=a).update(likes=F('likes') - 1)
        return redirect(reverse('post:question-detail', kwargs={'id': q}))
    else:
        answer_fav = AnswerFavourite.objects.create(answer=answer, user=user)
        answer_fav.save()
        Answer.objects.filter(pk=a).update(likes=F('likes') + 1)
        return redirect(reverse('post:question-detail', kwargs={'id': q}))


def home(request):
    questions = Question.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'home.html', context)
