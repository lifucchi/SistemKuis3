from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import  HttpResponse , request , response
# from django.views.generic import TemplateView
from django.views.generic import DetailView, ListView , View
# from quiz.serializers import QuizListSerializer, QuizDetailSerializer, UsersAnswerSerializer, QuizResultSerializer
from .models import Topic,Base_Competency,Core_Competency,Specific_Competency, Question, Answer, QuizTaker, UsersAnswer , Subject
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.db import transaction
from django.contrib import messages
from .forms import ChooseAnswerForm

class topicList (ListView):
    model = Topic
    # queryset = Question.objects.all()
    template_name = 'quiz/class-page.php'
    context_object_name = 'topic_list'

    def get_queryset(self):
        queryset = super(topicList, self).get_queryset()
        return queryset

@login_required()
def topicDetail (request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    bc = Base_Competency.objects.filter(topic=topic)
    return render(request, 'quiz/class-topic-page.php', {
        'topics': topic,
        'bcs': bc})


@login_required
def take_quiz(request, pk):
    student = request.user
    # messages.success(request, ('masuk'))
    try:
        quiz = Specific_Competency.objects.filter(base_Competency_id=pk).first()
        obj = QuizTaker.objects.create(user=student, specific_competency=quiz)
        quiz_taker = obj.pk
        question = quiz.indikator.filter(level__lte = 0.7)
        question = question.filter(level__gte=0.3)
        question = question.first()
        return redirect('question', quiz=quiz.pk, quiz_taker=quiz_taker, question_id=question.id)

    except Exception as e:
        quiz = "error"
        messages.success(request, ('Maaf, soal belum ditambahkan'))
        return redirect('topic')

def question(request,quiz,quiz_taker,question_id):
    student = QuizTaker.objects.get(pk=quiz_taker)
    question = Question.objects.get(pk=question_id)
    quiz = get_object_or_404(Specific_Competency, pk=quiz)

    if request.method == 'GET':
        question = Question.objects.get(pk=question_id)
        student = QuizTaker.objects.get(pk=quiz_taker)
        answered_questions = student.quiz_answers.count()
        answers = question.choices.all().order_by('?')

        choose_answer_form = ChooseAnswerForm()
        choose_answer_form.fields['answer'].queryset = answers

        context = {
                'question':question,
                'form': choose_answer_form,
                'answered_questions': answered_questions,
                # 'quiztaker' : student

            }

        return render(request, 'quiz/take_quiz_form.php', context)

    elif request.method == 'POST':
        choose_answer_form = ChooseAnswerForm(request.POST)
        if choose_answer_form.is_valid():
            answer = choose_answer_form.cleaned_data['answer']

            if answer.is_correct:
                grade = 1
            else:
                grade = 0

            response = UsersAnswer(
                quiztaker=student,
                question=question,
                answer=answer,
                grade=grade,
            )
            response.save()

            # score = UsersAnswer.objects.filter(quiztaker = quiz_taker).filter(answer__is_correct = 1),count()
            # score = UsersAnswer.objects.filter(quiztaker = quiz_taker)
            score = UsersAnswer.objects.filter(grade = 1).count()
            # score = UsersAnswer.grade.count()

            QuizTaker.objects.filter(pk=quiz_taker).update(score=score)

            #fuzzynya disini harusnya
            answered_questions = student.quiz_answers.count()

            if answered_questions % 5 == 0:
                # hitung fuzzy

                return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=question.id)

            else:
                if student.user.get_unanswered_questions(quiz).exists():
                    unanswered_questions = student.user.get_unanswered_questions(quiz)
                    question = unanswered_questions.first()
                else:
                    question = quiz.indikator.order_by('?')
                    question = question.first()

                return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=question.id)
