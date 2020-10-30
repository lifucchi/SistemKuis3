from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import  HttpResponse , request , response
# from django.views.generic import TemplateView
from django.views.generic import DetailView, ListView , View
# from quiz.serializers import QuizListSerializer, QuizDetailSerializer, UsersAnswerSerializer, QuizResultSerializer
from .models import Topic,Base_Competency,Core_Competency,Specific_Competency, Question, Answer, QuizTaker, UsersAnswer , Subject, QuizLog
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.db import transaction
from django.contrib import messages
from .forms import ChooseAnswerForm
from . import fuzzy

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
    bc = bc.filter(roll_out=1)
    return render(request, 'quiz/class-topic-page.php', {
        'topics': topic,
        'bcs': bc})


@login_required
def take_quiz(request, pk):
    student = request.user
    # messages.success(request, ('masuk'))
    try:
        quiz = Specific_Competency.objects.filter(base_Competency_id=pk).order_by('order').first()
        obj = QuizTaker.objects.create(user=student, specific_competency=quiz)
        quiz_taker = obj.pk
        question = quiz.indikator.filter(level__lte = 2)
        question = question.filter(level__gte= -1)
        question = question.order_by('?').first()
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
        # answers = question.choices.all().order_by('?')
        answers = question.choices.all()

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

            aresponse = UsersAnswer(
                quiztaker=student,
                question=question,
                answer=answer,
                grade=grade,
            )
            aresponse.save()

            #probabilitas
            #crips
            c = 0.25
            a = question.discrimination
            b = question.level
            r = grade
            #cek first ?

            queryset = QuizLog.objects.filter(quiztaker_id = quiz_taker)

            # try:
            #     # go = SomeModel.objects.get(foo='bar')
            #     # adakah = get_object_or_404(QuizLog, quiztaker_id=quiz_taker)
            #     # quizlogs = QuizLog.objects.filter(quiztaker_id=quiz_taker).last()
            #     quizlog = QuizLog.objects.get(id = quiz_taker)
            #     quizlog = QuizLog.objects.filter(quiztaker_id=quiz_taker).last()
            #     ada = 1
            # except QuizLog.DoesNotExist:
            #     ada = 0

            if queryset.exists():
                quizlogs = QuizLog.objects.filter(quiztaker_id=quiz_taker).last()
                bability = quizlogs.ql_ability
                p = c + (1 - c) * ((2.718 ** (1.7 * a * (bability - b))) / (1 + 2.718 ** (1.7 * a * (bability - b))))
                ################fuzzy#########################
                Hasil = fuzzy.fuzzy(a, b, p, r)
                deltaability = Hasil - bability

            else:
                p = 0.5
                ################fuzzy#########################
                Hasil = fuzzy.fuzzy(a, b, p, r)
                deltaability = 0


            if deltaability == 0 and queryset.exists():

                responselog = QuizLog(
                    questionlog=question_id,
                    ql_a=a,
                    ql_b=b,
                    ql_p=p,
                    ql_c=c,
                    ql_r=r,
                    ql_ability=Hasil,
                    ql_deltaability=deltaability,
                    quiztaker=student

                )

                responselog.save()

                # return render('quiz/class-topic-page.php', quiz=quiz.pk, quiz_taker=student.pk, question_id=question.id)

                topic = Topic.objects.get(pk=question.specific_Competency.base_Competency.topic.pk)
                # bcs = Base_Competency.objects.get(pk=question.specific_Competency.base_Competency.pk)
                bcs = Base_Competency.objects.filter(topic=topic)

                return render(request, 'quiz/class-topic-page.php', {
                    'topics': topic,
                    'bcs': bcs })
            else :

                responselog = QuizLog(
                    questionlog=question_id,
                    ql_a=a,
                    ql_b=b,
                    ql_p=p,
                    ql_c=c,
                    ql_r=r,
                    ql_ability=Hasil,
                    ql_deltaability=deltaability,
                    quiztaker=student

                )

                responselog.save()

                if student.user.get_unanswered_questions(quiz).exists():
                    unanswered_questions = student.user.get_unanswered_questions(quiz)
                    question = unanswered_questions.first()
                else:
                    question = quiz.indikator.order_by('?')
                    question = question.first()

                return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=question.id)



                # return render(request, 'quiz/class-topic-page.php', context)

            # score = UsersAnswer.objects.filter(quiztaker = quiz_taker).filter(answer__is_correct = 1),count()
            # score = UsersAnswer.objects.filter(quiztaker = quiz_taker)
            # score = UsersAnswer.objects.filter(grade = 1).count()
            # score = UsersAnswer.grade.count()

            # QuizTaker.objects.filter(pk=quiz_taker).update(score=score)

            #fuzzynya disini harusnya
            # answered_questions = student.quiz_answers.count()

            # if answered_questions % 5 == 0:
                # hitung fuzzy

                # return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=question.id)

            # else:
            #     if student.user.get_unanswered_questions(quiz).exists():
            #         unanswered_questions = student.user.get_unanswered_questions(quiz)
            #         question = unanswered_questions.first()
            #     else:
            #         question = quiz.indikator.order_by('?')
            #         question = question.first()
            #
            #     return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=question.id)
