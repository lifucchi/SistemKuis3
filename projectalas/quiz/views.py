from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import  HttpResponse , request , response
# from django.views.generic import TemplateView
from django.views.generic import DetailView, ListView , View
# from quiz.serializers import QuizListSerializer, QuizDetailSerializer, UsersAnswerSerializer, QuizResultSerializer
from .models import Topic,Base_Competency,ScoreDetil,Core_Competency,Specific_Competency, Question, Answer, QuizTaker, UsersAnswer , Subject, QuizLog
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
        obj = QuizTaker.objects.create(user=student)
        quiz_taker = obj.pk
        # question = quiz.indikator
        question = quiz.indikator.filter(level__lte = 2)
        question = question.filter(level__gte= -1)
        question = question.order_by('?').first()
        return redirect('question', quiz=quiz.pk, quiz_taker=quiz_taker, question_id=question.id)

    except Exception as e:
        quiz = "error"
        messages.success(request, ('Maaf, soal belum ditambahkan'))
        return redirect('topic')


##penentuan soal
# def penentuan ()

def question(request,quiz,quiz_taker,question_id):
    student = QuizTaker.objects.get(pk=quiz_taker)
    question = Question.objects.get(pk=question_id)
    quiz = get_object_or_404(Specific_Competency, pk=quiz)

    if request.method == 'GET':
        answered_questions = student.quiz_answers.count()
        answers = question.choices.all()
        choose_answer_form = ChooseAnswerForm()
        choose_answer_form.fields['answer'].queryset = answers

        context = {
                'question':question,
                'form': choose_answer_form,
                'answered_questions': answered_questions,
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

            ## PENENTUAN PEMILIHAN SOAL##

            #probabilitas
            #crips
            c = 0.25
            a = question.discrimination
            b = question.level
            r = grade
            #cek first ?

            queryset = QuizLog.objects.filter(quiztaker_id = quiz_taker)

            if queryset.exists():
                quizlogs = QuizLog.objects.filter(quiztaker_id=quiz_taker).last()
                bability = quizlogs.ql_ability
                p = c + (1 - c) * ((2.718 ** (1.7 * a * (bability - b))) / (1 + 2.718 ** (1.7 * a * (bability - b))))
                ################fuzzy#########################
                # Hasil = fuzzy.fuzzy(a, b, p, r)
                # Hasil = fuzzy.mfuzzy(a, b, p, r)
                hasil = fuzzy.mfuzzy(a, b, p, r)
                Hasil = hasil.fuzzy()

                deltaability = Hasil - bability

            else:
                p = 0.5
                ################fuzzy#########################
                # Hasil = fuzzy.fuzzy(a, b, p, r)
                # Hasil = fuzzy.mfuzzy(a, b, p, r)
                hasil = fuzzy.mfuzzy(a, b, p, r)
                Hasil = hasil.fuzzy()
                deltaability = 0


            #must know the score
            allquestion = UsersAnswer.objects.filter(quiztaker_id = quiz_taker).count()
            score = UsersAnswer.objects.filter(quiztaker_id  = quiz_taker)
            score = score.filter(grade = 1).count()
            totalscore = float(score)/float(allquestion)


            ###berakhir atau menuju next indikator?

            # if queryset.exists() and (deltaability == 0 or totalscore >= 0.7):
            if queryset.exists() and (deltaability == 0):
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

                ##save dulu kalau selesai 1 indikator
                # scoredetil = ScoreDetil.objects.create(user=student)
                # sc = question__

                scorenya = ScoreDetil(
                    specific_competency= quiz,
                    quiz_taker = student ,
                    desc = totalscore
                )
                scorenya.save()

                #CEK APAKAH ADA NEXT INDIKATOR?
                indikatornow = question.specific_Competency.order
                indikatornext = int(indikatornow)
                indikatorexist = Specific_Competency.objects.filter(pk = question.specific_Competency.pk ,order = indikatornext)

                if indikatorexist.exists():
                    if student.user.get_unanswered_questions(quiz).exists():
                        unanswered_questions = student.user.get_unanswered_questions(quiz)
                        # unanswered_questions = unanswered_questions.filter(specific_Competency__order=indikatornext)
                        unanswered_questions = unanswered_questions.filter(level__lte=2)
                        unanswered_questions = unanswered_questions.filter(level__gte=-1)
                        question = unanswered_questions.first()
                    else:
                        # question = indikatorexist.indikator.filter(level__lte=2)
                        # question = question.indikator.filter(level__gte=-1)
                        # question = question.first()
                        question = quiz.indikator.order_by('?')
                        question = question.first()

                    return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=question.id)
                else:
                    topic = Topic.objects.get(pk=question.specific_Competency.base_Competency.topic.pk)
                    # bcs = Base_Competency.objects.get(pk=question.specific_Competency.base_Competency.pk)
                    bcs = Base_Competency.objects.filter(topic=topic)
                    bcs = bcs.filter(roll_out=1)

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

                if allquestion < 6 :
                    if student.user.get_unanswered_questions(quiz).exists():
                        unanswered_questions = student.user.get_unanswered_questions(quiz)
                        question = unanswered_questions.first()
                    else:
                        question = quiz.indikator.order_by('?')
                        question = question.first()

                    return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=question.id)

                else :
                    scorenya = ScoreDetil(
                        specific_competency=quiz,
                        quiz_taker=student,
                        desc=totalscore
                    )
                    scorenya.save()

                    # CEK APAKAH ADA NEXT INDIKATOR?
                    indikatornow = question.specific_Competency.order
                    indikatornext = int(indikatornow)
                    indikatorexist = Specific_Competency.objects.filter(pk=question.specific_Competency.pk, order=indikatornext)

                    if indikatorexist.exists():
                        if student.user.get_unanswered_questions(quiz).exists():
                            unanswered_questions = student.user.get_unanswered_questions(quiz)
                            # unanswered_questions = unanswered_questions.filter(specific_Competency__order=indikatornext)
                            unanswered_questions = unanswered_questions.filter(level__lte=2)
                            unanswered_questions = unanswered_questions.filter(level__gte=-1)
                            question = unanswered_questions.first()
                        else:
                            # question = indikatorexist.indikator.filter(level__lte=2)
                            # question = question.indikator.filter(level__gte=-1)
                            # question = question.first()
                            question = quiz.indikator.order_by('?')
                            question = question.first()

                        return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=question.id)
                    else:
                        topic = Topic.objects.get(pk=question.specific_Competency.base_Competency.topic.pk)
                        # bcs = Base_Competency.objects.get(pk=question.specific_Competency.base_Competency.pk)
                        bcs = Base_Competency.objects.filter(topic=topic)
                        bcs = bcs.filter(roll_out=1)

                        return render(request, 'quiz/class-topic-page.php', {
                            'topics': topic,
                            'bcs': bcs})

                    # return render('quiz/class-topic-page.php', quiz=quiz.pk, quiz_taker=student.pk, question_id=question.id)

                    # topic = Topic.objects.get(pk=question.specific_Competency.base_Competency.topic.pk)
                    # # bcs = Base_Competency.objects.get(pk=question.specific_Competency.base_Competency.pk)
                    # bcs = Base_Competency.objects.filter(topic=topic)
                    # bcs = bcs.filter(roll_out=1)
                    #
                    # return render(request, 'quiz/class-topic-page.php', {
                    #     'topics': topic,
                    #     'bcs': bcs})

                # return render(request, 'quiz/class-topic-page.php', context)

