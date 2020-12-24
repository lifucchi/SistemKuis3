from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView , View
from .models import Topic,Base_Competency,ScoreDetil,Core_Competency,Specific_Competency, Question, Answer, QuizTaker, UsersAnswer , Subject, QuizLog
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import ChooseAnswerForm
from . import selecting
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Prefetch
from django.urls import reverse
from django.utils import timezone
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

    def take_quiz(request, pk):
        student = request.user
        # messages.success(request, ('masuk'))
        try:
            quiz = Specific_Competency.objects.filter(base_Competency_id=pk, roll_out = 1).order_by('order').first()
            obj = QuizTaker.objects.create(user=student)
            quiz_taker = obj.pk
            # question = quiz.indikator
            question = quiz.indikator.filter(level__lte=2)
            question = question.filter(level__gte=-1)
            question = question.order_by('?').first()

            if (question is not None):
                return redirect('question', quiz=quiz.pk, quiz_taker=quiz_taker, question_id=question.id)
            else:
                return redirect('topics', pk=pk)


        except Exception as e:
            quiz = "error"
            messages.success(request, ('Maaf, soal belum ditambahkan'))
            return redirect('topics', pk=pk)

    def question(request, quiz, quiz_taker, question_id):
        student = QuizTaker.objects.get(pk=quiz_taker)
        question = Question.objects.get(pk=question_id)
        quiz = get_object_or_404(Specific_Competency, pk=quiz)

        if request.method == 'GET':
            answered_questions = student.quiz_answers.count()
            # answers = question.choices.all()
            answers = question.choices.all().order_by('?')
            choose_answer_form = ChooseAnswerForm()
            choose_answer_form.fields['answer'].queryset = answers

            context = {
                'question': question,
                'form': choose_answer_form,
                'answered_questions': answered_questions,
            }
            return render(request, 'quiz/take_quiz_form.php', context)

        elif request.method == 'POST':
            verifikasi = request.POST.get('verifikasi', 0)
            menghitung = selecting.Menghitung(quiz_taker, quiz, question)
            penentuan = selecting.Penentuan()
            pertanyaan = selecting.PemilihanKemampuan(quiz, student)

            if(verifikasi == 1 or verifikasi == "1"):
                values = []
                for key in list(request.POST.keys()):
                    if (key == "verifikasi" or key == "csrfmiddlewaretoken"):
                        continue
                    UsersAnswer.objects.filter(id=key).update(nebak=request.POST[key])

                Scorenya = menghitung.menghitungScoreKeseluruhan()
                Scorenya = (round(Scorenya, 2))
                QuizTaker.objects.filter(pk=quiz_taker).update(score=Scorenya)
                QuizTaker.objects.filter(pk=quiz_taker).update(date_finished=timezone.now())
                                        # MASUKKAN NILAI DISINI
                return redirect(reverse('score', kwargs={'pk': quiz_taker,
                                                            'bc': question.specific_Competency.base_Competency.pk}))

            choose_answer_form = ChooseAnswerForm(request.POST)


            # JIKA MENGISI JAWABAN
            if choose_answer_form.is_valid():
                answer = choose_answer_form.cleaned_data['answer']
                if answer.is_correct:
                    grade = 1
                else:
                    grade = 0

                aresponse = UsersAnswer(
                    quiztaker=student,
                    # question=question,
                    endtime = request.POST['endtime'],
                    starttime=request.POST['starttime'],
                    answer=answer,
                    grade=grade,
                )
                aresponse.save()

                ## PENENTUAN PEMILIHAN SOAL##

                # crips
                c = 0.25
                a = question.discrimination
                b = question.level
                r = grade

                # membuat class menghitung ?
                # FUZZY
                queryset, p, Hasil, deltaability = menghitung.menghitungFuzzy(a, b, c, r)

                # must know the score
                totalscore, allquestion = menghitung.menghitungScoreIndikator()
                ###berakhir atau menuju next indikator?

                # CEK APAKAH ADA NEXT INDIKATOR?
                # pakaiclass

                if queryset.exists() and (deltaability == 0):
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

                    ##save dulu kalau selesai 1 indikator
                    scorenya = ScoreDetil(
                        specific_competency=quiz,
                        quiz_taker=student,
                        desc=totalscore
                    )
                    scorenya.save()

                    # #CEK APAKAH ADA NEXT INDIKATOR?
                    indikatorexist, ordernext = menghitung.menghitungIndikator()

                    if indikatorexist.exists():
                        nextIndikator = penentuan.newIndikator(question.specific_Competency.base_Competency.pk,
                                                               ordernext)
                        if student.user.get_unanswered_questions(nextIndikator).exists():
                            newquestion = penentuan.indikatorNext(nextIndikator, student)
                            return redirect('question', quiz=nextIndikator.pk, quiz_taker=student.pk,
                                            question_id=newquestion.pk)
                        else:
                            context = {
                                'indikatornext': "soal tidak ditemukan",
                            }
                            return render(request, 'quiz/quiz_result2.php', context)
                    else:
                        # Hitung score
                        all_answered_questions = UsersAnswer.objects.filter(quiztaker=student, nebak__isnull=True)
                        if len(all_answered_questions) != 0:
                            squestion = []
                            for useranswer in all_answered_questions:
                                question = useranswer.answer.question
                                choices = question.choices.all().order_by("?")
                                squestion.append({
                                    'question': question,
                                    'choices' : choices,
                                    'answer'  : useranswer
                                })

                            return render(request, 'quiz/verifikasijawaban.php', {
                                'useranswer' : squestion
                            })


                        Scorenya = menghitung.menghitungScoreKeseluruhan()
                        Scorenya = (round(Scorenya, 2))

                        QuizTaker.objects.filter(pk=quiz_taker).update(score=Scorenya)
                        QuizTaker.objects.filter(pk=quiz_taker).update(date_finished=timezone.now())

                        # MASUKKAN NILAI DISINI
                        return redirect(reverse('score', kwargs={'pk': quiz_taker,
                                                                 'bc': question.specific_Competency.base_Competency.pk}))
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

                    if allquestion < 6:

                        # memberikan soal sesuai dengan kemampuan
                        newQuestion, var = pertanyaan.soalKemampuan(Hasil)
                        # newQuestion, var = soalKemampuan(Hasil, quiz, student)

                        if newQuestion.exists():
                            newquestion = newQuestion.first()

                            return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=newquestion.id)

                        else:
                            context = {
                                'indikatornext': "SOALNYA TIDAK ADA",
                                'vars': var

                            }
                            return render(request, 'quiz/quiz_result2.php', context)


                    else:
                        scorenya = ScoreDetil(
                            specific_competency=quiz,
                            quiz_taker=student,
                            desc=totalscore
                        )
                        scorenya.save()

                        indikatorexist, ordernext = menghitung.menghitungIndikator()

                        if indikatorexist.exists():
                            nextIndikator = penentuan.newIndikator(question.specific_Competency.base_Competency.pk,
                                                                   ordernext)
                            if student.user.get_unanswered_questions(nextIndikator).exists():

                                newquestion = penentuan.indikatorNext(nextIndikator, student)
                                return redirect('question', quiz=nextIndikator.pk, quiz_taker=student.pk,
                                                question_id=newquestion.pk)

                            else:
                                context = {
                                    'indikatornext': "SOALNYA HABIIIIIISSSSSSSSSS",
                                }
                                return render(request, 'quiz/quiz_result2.php', context)
                        else:
                            # Hitung score
                            all_answered_questions = UsersAnswer.objects.filter(quiztaker=student, nebak__isnull=True)
                            if len(all_answered_questions) != 0:
                                squestion = []
                                for useranswer in all_answered_questions:
                                    question = useranswer.answer.question
                                    choices = question.choices.all().order_by("?")
                                    squestion.append({
                                        'question': question,
                                        'choices' : choices,
                                        'answer'  : useranswer
                                    })

                                return render(request, 'quiz/verifikasijawaban.php', {
                                    'useranswer' : squestion
                                })

                            Scorenya = menghitung.menghitungScoreKeseluruhan()
                            Scorenya = (round(Scorenya, 2))
                            QuizTaker.objects.filter(pk=quiz_taker).update(score=Scorenya)
                            QuizTaker.objects.filter(pk=quiz_taker).update(date_finished=timezone.now())

                            # MASUKKAN NILAI DISINI

                            # return render('quiz/page-quiz_result.php', context)
                            return redirect(reverse('score', kwargs={'pk': quiz_taker,
                                                                     'bc': question.specific_Competency.base_Competency.pk}))

            else:
                messages.error(request, "tolong pilih jawaban")
                # grade = 0
                #
                # aresponse = UsersAnswer(
                #     quiztaker=student,
                #     # question=question,
                #     endtime = request.POST['endtime'],
                #     starttime=request.POST['starttime'],
                #     answer=None,
                #     grade=grade,
                # )
                # aresponse.save()
                #
                # ## PENENTUAN PEMILIHAN SOAL##
                #
                # # crips
                # c = 0.25
                # a = question.discrimination
                # b = question.level
                # r = grade
                #
                # # FUZZY
                # queryset, p, Hasil, deltaability = menghitung.menghitungFuzzy(a, b, c, r)
                #
                # # must know the score
                # totalscore, allquestion = menghitung.menghitungScoreIndikator()
                #
                # ###berakhir atau menuju next indikator?
                #
                # # CEK APAKAH ADA NEXT INDIKATOR?
                #
                #
                # if queryset.exists() and (deltaability == 0):
                #     responselog = QuizLog(
                #         questionlog=question_id,
                #         sclog=quiz.id,
                #         ql_a=a,
                #         ql_b=b,
                #         ql_p=p,
                #         ql_c=c,
                #         ql_r=r,
                #         ql_ability=Hasil,
                #         ql_deltaability=deltaability,
                #         quiztaker=student
                #     )
                #     responselog.save()
                #
                #     ##save dulu kalau selesai 1 indikator
                #     scorenya = ScoreDetil(
                #         specific_competency=quiz,
                #         quiz_taker=student,
                #         desc=totalscore
                #     )
                #     scorenya.save()
                #
                #     # #CEK APAKAH ADA NEXT INDIKATOR?
                #     indikatorexist, ordernext = menghitung.menghitungIndikator()
                #
                #     if indikatorexist.exists():
                #         nextIndikator = penentuan.newIndikator(question.specific_Competency.base_Competency.pk,
                #                                                ordernext)
                #         if student.user.get_unanswered_questions(nextIndikator).exists():
                #             newquestion = penentuan.indikatorNext(nextIndikator, student)
                #             return redirect('question', quiz=nextIndikator.pk, quiz_taker=student.pk,
                #                             question_id=newquestion.pk)
                #
                #         else:
                #             context = {
                #                 'indikatornext': "soal tidak ditemukan",
                #             }
                #             return render(request, 'quiz/quiz_result2.php', context)
                #     else:
                #         # Hitung score
                #         all_answered_questions = UsersAnswer.objects.filter(quiztaker=student, nebak__isnull=True)
                #         if len(all_answered_questions) != 0:
                #             squestion = []
                #             for useranswer in all_answered_questions:
                #                 question = useranswer.answer.question
                #                 choices = question.choices.all().order_by("?")
                #                 squestion.append({
                #                     'question': question,
                #                     'choices' : choices,
                #                     'answer'  : useranswer
                #                 })
                #
                #             return render(request, 'quiz/verifikasijawaban.php', {
                #                 'useranswer' : squestion
                #             })
                #
                #         Scorenya = menghitung.menghitungScoreKeseluruhan()
                #         Scorenya = (round(Scorenya, 2))
                #         QuizTaker.objects.filter(pk=quiz_taker).update(score=Scorenya)
                #         QuizTaker.objects.filter(pk=quiz_taker).update(date_finished=timezone.now())
                #
                #         # MASUKKAN NILAI DISINI
                #         return redirect(reverse('score', kwargs={'pk': quiz_taker,
                #                                                  'bc': question.specific_Competency.base_Competency.pk}))
                # else:
                #     responselog = QuizLog(
                #         questionlog=question_id,
                #         sclog=quiz.id,
                #         ql_a=a,
                #         ql_b=b,
                #         ql_p=p,
                #         ql_c=c,
                #         ql_r=r,
                #         ql_ability=Hasil,
                #         ql_deltaability=deltaability,
                #         quiztaker=student
                #
                #     )
                #
                #     responselog.save()
                #
                #     if allquestion < 6:
                #
                #         # memberikan soal sesuai dengan kemampuan
                #         newQuestion, var = pertanyaan.soalKemampuan(Hasil)
                #         # newQuestion, var = soalKemampuan(Hasil, quiz, student)
                #
                #         if newQuestion.exists():
                #             # unanswered_questions = student.user.get_unanswered_questions(quiz)
                #             newquestion = newQuestion.first()
                #
                #             return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=newquestion.id)
                #
                #         else:
                #             # question = quiz.indikator.order_by('?')
                #             # question = question.first()
                #
                #             context = {
                #                 'indikatornext': "SOALNYA TIDAK ADA",
                #                 'vars': var
                #
                #             }
                #             return render(request, 'quiz/quiz_result2.php', context)
                #
                #
                #     else:
                #         scorenya = ScoreDetil(
                #             specific_competency=quiz,
                #             quiz_taker=student,
                #             desc=totalscore
                #         )
                #         scorenya.save()
                #
                #         indikatorexist, ordernext = menghitung.menghitungIndikator()
                #
                #         if indikatorexist.exists():
                #             nextIndikator = penentuan.newIndikator(question.specific_Competency.base_Competency.pk,
                #                                                    ordernext)
                #             if student.user.get_unanswered_questions(nextIndikator).exists():
                #
                #                 newquestion = penentuan.indikatorNext(nextIndikator, student)
                #                 return redirect('question', quiz=nextIndikator.pk, quiz_taker=student.pk,
                #                                 question_id=newquestion.pk)
                #
                #             else:
                #
                #                 context = {
                #                     'indikatornext': "SOALNYA HABIIIIIISSSSSSSSSS",
                #                 }
                #                 return render(request, 'quiz/quiz_result2.php', context)
                #         else:
                #             # Hitung score
                #             all_answered_questions = UsersAnswer.objects.filter(quiztaker=student, nebak__isnull=True)
                #             if len(all_answered_questions) != 0:
                #                 squestion = []
                #                 for useranswer in all_answered_questions:
                #                     question = useranswer.answer.question
                #                     choices = question.choices.all().order_by("?")
                #                     squestion.append({
                #                         'question': question,
                #                         'choices' : choices,
                #                         'answer'  : useranswer
                #                     })
                #
                #                 return render(request, 'quiz/verifikasijawaban.php', {
                #                     'useranswer' : squestion
                #                 })
                #             Scorenya = menghitung.menghitungScoreKeseluruhan()
                #             Scorenya = (round(Scorenya, 2))
                #             QuizTaker.objects.filter(pk=quiz_taker).update(score=Scorenya)
                #             QuizTaker.objects.filter(pk=quiz_taker).update(date_finished=timezone.now())
                #
                #             # MASUKKAN NILAI DISINI
                #             return redirect(reverse('score', kwargs={'pk': quiz_taker,
                #                                                      'bc': question.specific_Competency.base_Competency.pk}))


class ScoresList(LoginRequiredMixin, ListView ):
    model = QuizTaker
    template_name = 'quiz/page-score_quiz_result.php'
    context_object_name = 'mark_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user
        context['fullscore'] = QuizTaker.objects.filter(user_id = student.pk).prefetch_related(
                Prefetch('quiz_taker', queryset=ScoreDetil.objects.filter(specific_competency__base_Competency_id = self.kwargs['pk']))
            ).distinct()
        context['bcs'] = Base_Competency.objects.get(pk = self.kwargs['pk'] )
        # context['fullscore'] = QuizTaker.objects.prefetch_related('quiz_taker')
        # context['fullscore'] =  context['fullscore'].filter(user_id = student.pk, quiz_taker__specific_competency__base_Competency_id = self.kwargs['pk'])
        context = {'fullscore': context['fullscore'], 'bcs' : context['bcs'] }
        return context

class ScoreList(LoginRequiredMixin,ListView ):
    model = Base_Competency
    template_name = 'quiz/page-quiz_result.php'
    context_object_name = 'mark_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fullscore'] = QuizTaker.objects.filter(pk=self.kwargs['pk']).prefetch_related(
            Prefetch('quiz_taker',
                     queryset=ScoreDetil.objects.filter(specific_competency__base_Competency_id=self.kwargs['bc']))
        ).distinct()
        context['bcs'] = Base_Competency.objects.get(pk = self.kwargs['bc'] )

        context = {'fullscore': context['fullscore'], 'bcs' : context['bcs'] }
        return context


#########################################################################################################################################
