from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import  HttpResponse , request , response
# from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView , View
# from quiz.serializers import QuizListSerializer, QuizDetailSerializer, UsersAnswerSerializer, QuizResultSerializer
from .models import Topic,Base_Competency,ScoreDetil,Core_Competency,Specific_Competency, Question, Answer, QuizTaker, UsersAnswer , Subject, QuizLog
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.db import transaction
from django.contrib import messages
from .forms import ChooseAnswerForm, QuizTakerForm
from . import fuzzy
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.db.models import Avg

# decorators = [never_cache, login_required]

class SubjectsList(LoginRequiredMixin,ListView):
    model = Subject

    template_name = 'quiz/page-subject.php'
    context_object_name = 'subject_list'

    def get_queryset(self):
        queryset = super(SubjectsList, self).get_queryset()
        return queryset

class ClassList(LoginRequiredMixin,DetailView):
    model = Subject
    template_name = 'quiz/page-class.php'
    context_object_name = 'class_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk'])
        context['ccs'] = Core_Competency.objects.filter(subject_id= self.kwargs['pk'])
        return context

class TopicList (LoginRequiredMixin,DetailView):
    model = Core_Competency
    # queryset = Question.objects.all()
    template_name = 'quiz/page-topic.php'
    context_object_name = 'topic_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['subject'] = get_object_or_404(Subject, pk=self.kwargs['pk'])
        context['bcs'] = Base_Competency.objects.filter(core_Competency_id=self.kwargs['pk'])
        if context['bcs'].count() > 0:
            context['topic_name'] = context['bcs'][0].topic.name
        else:
            pass
        return context

# class TopicList (LoginRequiredMixin,ListView):
#     model = Topic
#     # queryset = Question.objects.all()
#     template_name = 'quiz/class-page.php'
#     context_object_name = 'topic_list'
#
#     def get_queryset(self):
#         queryset = super(TopicList, self).get_queryset()
#         return queryset

# @login_required()
# def topicDetail (request, slug):
#     topic = get_object_or_404(Topic, slug=slug)
#     bc = Base_Competency.objects.filter(topic=topic)
#     bc = bc.filter(roll_out=1)
#     return render(request, 'quiz/class-topic-page.php', {
#         'topics': topic,
#         'bcs': bc})

class TopicDetailView(LoginRequiredMixin,DetailView):
    model = Topic
    template_name = 'quiz/class-topic-page.php'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = get_object_or_404(Topic, slug=self.kwargs['slug'])
        context['bcs'] = Base_Competency.objects.filter(topic= context['topics'].pk ).filter(roll_out=1)
        return context


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
        return redirect('topics', pk = pk)

##penentuan soal

def menghitungIndikator(question):
    indikatornow = question.specific_Competency.order
    indikatornext = int(indikatornow) + 1
    ordernext = int(indikatornext)
    indikatorexist = Base_Competency.objects.filter(pk=question.specific_Competency.base_Competency.pk,  k_dasar__order=ordernext)
    return indikatorexist,ordernext

def menghitungScoreIndikator(quiz_taker,indikator):
    allquestion = UsersAnswer.objects.filter(quiztaker_id=quiz_taker, question__specific_Competency__pk = indikator ).count()
    score = UsersAnswer.objects.filter(quiztaker_id=quiz_taker, question__specific_Competency__pk = indikator, grade=1).count()
    totalscore = float(score) / float(allquestion)
    return totalscore, allquestion

def menghitungScoreKeseluruhan(quiz_taker):
    scoreDetails = ScoreDetil.objects.filter(quiz_taker_id=quiz_taker).aggregate(Avg('desc'))['desc__avg']
    return float(scoreDetails)

def menghitungFuzzy(quiz_taker,quiz,a,b,c,r):
    queryset = QuizLog.objects.filter(quiztaker_id=quiz_taker, sclog = quiz.id)
    # detilskor = ScoreDetil.objects.filter(quiz_taker_id=quiz_taker, specific_competency_id = quiz.pk)

    if queryset.exists() :
        quizlogs = QuizLog.objects.filter(quiztaker_id=quiz_taker).last()
        bability = quizlogs.ql_ability
        p = c + (1 - c) * ((2.718 ** (1.7 * a * (bability - b))) / (1 + 2.718 ** (1.7 * a * (bability - b))))
        ################fuzzy#########################
        hasil = fuzzy.Mfuzzy(a, b, p, r)
        Hasil = hasil.fuzzy()
        deltaability = Hasil - bability
    else:
        p = 0.5
        hasil = fuzzy.Mfuzzy(a, b, p, r)
        Hasil = hasil.fuzzy()
        deltaability = 0

    return queryset, p,Hasil, deltaability

def indikatorNext(quiz, student):
    unanswered_questions = student.user.get_unanswered_questions(quiz)
    unanswered_questions = unanswered_questions.filter(level__lte=2,level__gte=-1)
    question = unanswered_questions.first()
    return question

def newIndikator(indikatorexist,ordernext):
    nextIndikator = get_object_or_404(Specific_Competency, order = ordernext , base_Competency_id = indikatorexist )
    return nextIndikator

def soalKemampuan(Hasil, quiz,student):
    satuindikator = student.user.get_unanswered_questions(quiz)
    #verylow
    if Hasil < -0.5:
        satuindikator = satuindikator.filter(level__lte=-1,level__gte=-3)
        var ="verylow"
    #Low
    elif Hasil > -1 and Hasil < 0.5:
        satuindikator = satuindikator.filter(level__lte=0, level__gte=-1)
        var ="low"

    #Averange
    elif Hasil >0 and Hasil < 1.5:
        satuindikator = satuindikator.filter(level__lte=1,level__gte=0)
        var ="Averange"

    #good
    elif Hasil > 0.5 and Hasil < 2:
        satuindikator = satuindikator.filter(level__lte=2, level__gte=1)
        var ="good"


    #excellent
    elif Hasil > 1.5:
        satuindikator = satuindikator.filter(level__gte=2)
        var = "excelent"

    return satuindikator , var




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
        #JIKA MENGISI JAWABAN
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

            #crips
            c = 0.25
            a = question.discrimination
            b = question.level
            r = grade

            #FUZZY
            queryset, p,Hasil, deltaability = menghitungFuzzy(quiz_taker,quiz, a, b, c, r)

            #must know the score
            totalscore, allquestion = menghitungScoreIndikator(quiz_taker,question.specific_Competency.pk)

            ###berakhir atau menuju next indikator?

            # CEK APAKAH ADA NEXT INDIKATOR?
            indikatorexist,ordernext = menghitungIndikator(question)

            if queryset.exists()  and (deltaability == 0):
                responselog = QuizLog(
                    questionlog=question_id,
                    sclog = quiz.id,
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
                scorenya = ScoreDetil(
                    specific_competency= quiz,
                    quiz_taker = student ,
                    desc = totalscore
                )
                scorenya.save()

                # #CEK APAKAH ADA NEXT INDIKATOR?
                # indikatorexist,indikatornext,indikatornow  = menghitungIndikator(question)

                if indikatorexist.exists():
                    nextIndikator = newIndikator(question.specific_Competency.base_Competency.pk,ordernext)
                    if student.user.get_unanswered_questions(nextIndikator).exists():
                        newquestion = indikatorNext(nextIndikator, student)
                        return redirect('question', quiz=nextIndikator.pk, quiz_taker=student.pk, question_id=newquestion.pk)

                    else:
                        context = {
                            'indikatornext': "soal tidak ditemukan",
                        }
                        return render(request, 'quiz/quiz_result2.php', context)
                else:
                    # Hitung score
                    Scorenya = menghitungScoreKeseluruhan(quiz_taker)
                    Scorenya = (round(Scorenya, 2))
                    QuizTaker.objects.filter(pk=quiz_taker).update(score=Scorenya)
                    # MASUKKAN NILAI DISINI
                    context = {
                        'indikatornext': (Scorenya*100),

                    }
                    return render(request, 'quiz/quiz_result.php', context)
            else:
                responselog = QuizLog(
                    questionlog=question_id,
                    sclog=quiz.id,
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

                    #memberikan soal sesuai dengan kemampuan
                    newQuestion, var = soalKemampuan(Hasil, quiz, student)

                    if newQuestion.exists():
                        # unanswered_questions = student.user.get_unanswered_questions(quiz)
                        newquestion = newQuestion.first()

                        return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=newquestion.id)

                    else:
                        # question = quiz.indikator.order_by('?')
                        # question = question.first()

                        context = {
                            'indikatornext': "SOALNYA TIDAK ADA",
                            'vars' : var

                        }
                        return render(request, 'quiz/quiz_result2.php', context)


                else :
                    scorenya = ScoreDetil(
                        specific_competency=quiz,
                        quiz_taker=student,
                        desc=totalscore
                    )
                    scorenya.save()

                    if indikatorexist.exists():
                        nextIndikator = newIndikator(question.specific_Competency.base_Competency.pk, ordernext)
                        if student.user.get_unanswered_questions(nextIndikator).exists():

                            newquestion = indikatorNext(nextIndikator, student)
                            return redirect('question', quiz=nextIndikator.pk, quiz_taker=student.pk,
                                            question_id=newquestion.pk)

                        else:
                            context = {
                                'indikatornext': "SOALNYA HABIIIIIISSSSSSSSSS",
                            }
                            return render(request, 'quiz/quiz_result2.php', context)
                    else:
                        # Hitung score
                        Scorenya = menghitungScoreKeseluruhan(quiz_taker)
                        Scorenya = (round(Scorenya, 2))
                        QuizTaker.objects.filter(pk=quiz_taker).update(score=Scorenya)
                        # MASUKKAN NILAI DISINI
                        context = {
                            'indikatornext': (Scorenya * 100),

                        }
                        return render(request, 'quiz/quiz_result.php', context)

        else:
            grade = 0

            aresponse = UsersAnswer(
                quiztaker=student,
                question=question,
                answer= None,
                grade=grade,
            )
            aresponse.save()


            ## PENENTUAN PEMILIHAN SOAL##

            #crips
            c = 0.25
            a = question.discrimination
            b = question.level
            r = grade

            #FUZZY
            queryset, p,Hasil, deltaability = menghitungFuzzy(quiz_taker,quiz, a, b, c, r)

            #must know the score
            totalscore, allquestion = menghitungScoreIndikator(quiz_taker,question.specific_Competency.pk)

            ###berakhir atau menuju next indikator?

            # CEK APAKAH ADA NEXT INDIKATOR?
            indikatorexist,ordernext = menghitungIndikator(question)

            if queryset.exists()  and (deltaability == 0):
                responselog = QuizLog(
                    questionlog=question_id,
                    sclog = quiz.id,
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
                scorenya = ScoreDetil(
                    specific_competency= quiz,
                    quiz_taker = student ,
                    desc = totalscore
                )
                scorenya.save()

                # #CEK APAKAH ADA NEXT INDIKATOR?
                # indikatorexist,indikatornext,indikatornow  = menghitungIndikator(question)

                if indikatorexist.exists():
                    nextIndikator = newIndikator(question.specific_Competency.base_Competency.pk,ordernext)
                    if student.user.get_unanswered_questions(nextIndikator).exists():
                        newquestion = indikatorNext(nextIndikator, student)
                        return redirect('question', quiz=nextIndikator.pk, quiz_taker=student.pk, question_id=newquestion.pk)

                    else:
                        context = {
                            'indikatornext': "soal tidak ditemukan",
                        }
                        return render(request, 'quiz/quiz_result2.php', context)
                else:
                    # Hitung score
                    Scorenya = menghitungScoreKeseluruhan(quiz_taker)
                    Scorenya = (round(Scorenya, 2))
                    QuizTaker.objects.filter(pk=quiz_taker).update(score=Scorenya)
                    # MASUKKAN NILAI DISINI
                    context = {
                        'indikatornext': (Scorenya * 100),

                    }
                    return render(request, 'quiz/quiz_result.php', context)
            else:
                responselog = QuizLog(
                    questionlog=question_id,
                    sclog=quiz.id,
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

                    #memberikan soal sesuai dengan kemampuan
                    newQuestion, var = soalKemampuan(Hasil, quiz, student)

                    if newQuestion.exists():
                        # unanswered_questions = student.user.get_unanswered_questions(quiz)
                        newquestion = newQuestion.first()

                        return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=newquestion.id)

                    else:
                        # question = quiz.indikator.order_by('?')
                        # question = question.first()

                        context = {
                            'indikatornext': "SOALNYA TIDAK ADA",
                            'vars' : var

                        }
                        return render(request, 'quiz/quiz_result2.php', context)


                else :
                    scorenya = ScoreDetil(
                        specific_competency=quiz,
                        quiz_taker=student,
                        desc=totalscore
                    )
                    scorenya.save()

                    if indikatorexist.exists():
                        nextIndikator = newIndikator(question.specific_Competency.base_Competency.pk, ordernext)
                        if student.user.get_unanswered_questions(nextIndikator).exists():

                            newquestion = indikatorNext(nextIndikator, student)
                            return redirect('question', quiz=nextIndikator.pk, quiz_taker=student.pk,
                                            question_id=newquestion.pk)

                        else:
                            context = {
                                'indikatornext': "SOALNYA HABIIIIIISSSSSSSSSS",
                            }
                            return render(request, 'quiz/quiz_result2.php', context)
                    else:
                        # Hitung score
                        Scorenya = menghitungScoreKeseluruhan(quiz_taker)
                        Scorenya = (round(Scorenya, 2))
                        QuizTaker.objects.filter(pk=quiz_taker).update(score=Scorenya)
                        # MASUKKAN NILAI DISINI
                        context = {
                            'indikatornext': (Scorenya * 100),

                        }
                        return render(request, 'quiz/quiz_result.php', context)




# class TakeQuiz(LoginRequiredMixin,CreateView):
#     model = QuizTaker
#     fields = ['user']
#     # form_class = QuizTakerForm
#     template_name = 'quiz/class-topic-page.php'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
#
#     # def get_queryset(self):
#         # student = self.request.user
#         # self.quiz = Specific_Competency.objects.filter(base_Competency_id=self.kwargs['pk']).order_by('order').first()
#         # self.question = self.quiz.indikator.filter(level__lte = 2, level__gte= -1).order_by('?').first()
#         # return self.user.post_set.order_by('-id')
#
#     def get_context_data(self, **kwargs):
#         # student = self.request.user
#         context = super().get_context_data(**kwargs)
#         context['quiz'] = Specific_Competency.objects.filter(base_Competency_id=self.kwargs['pk']).order_by('order').first()
#         # obj = QuizTaker.objects.create(user=student)
#         # context['quiz_taker'] = obj.pk
#         ##question
#         context['question'] = context['quiz'].indikator.filter(level__lte = 2, level__gte= -1).order_by('?').first()
#         # context['quiz'] = self.quiz
#         # context['question'] = self.question
#         return context
#
#     def get_success_url(self):
#         quiz = Specific_Competency.objects.filter(base_Competency_id=self.kwargs['pk']).order_by('order').first()
#         question = self.quiz.indikator.filter(level__lte = 2, level__gte= -1).order_by('?').first()
#         return redirect('question', quiz = quiz.pk, quiz_taker=self.object.id, question_id= question.id)
#
