from .models import Topic,Base_Competency,ScoreDetil,Core_Competency,Specific_Competency, Question, Answer, QuizTaker, UsersAnswer , Subject, QuizLog
from django.db.models import Avg, Prefetch
from . import fuzzy
from django.shortcuts import get_object_or_404


class Penentuan:
    def indikatorNext(self,quiz, student):
        unanswered_questions = student.user.get_unanswered_questions(quiz)
        unanswered_questions = unanswered_questions.filter(level__lte=2, level__gte=-1)
        question = unanswered_questions.first()
        return question

    def newIndikator(self,indikatorexist, ordernext):
        nextIndikator = get_object_or_404(Specific_Competency, order=ordernext, base_Competency_id=indikatorexist)
        return nextIndikator

class Menghitung:
    def __init__(self ,quiz_taker, quiz, question):
        self.question = question
        self.quiz_taker = quiz_taker
        self.indikator = question.specific_Competency.pk
        self.quiz = quiz

    def menghitungFuzzy(self, a, b, c, r):
        queryset = QuizLog.objects.filter(quiztaker_id=self.quiz_taker, sclog=self.quiz.id)
        if queryset.exists():
            quizlogs = QuizLog.objects.filter(quiztaker_id=self.quiz_taker).last()
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

        return queryset, p, Hasil, deltaability

    def menghitungScoreIndikator(self):
        allquestion = UsersAnswer.objects.filter(quiztaker_id=self.quiz_taker,
                                                 answer__question__specific_Competency__pk=self.indikator).count()
        score = UsersAnswer.objects.filter(quiztaker_id=self.quiz_taker, answer__question__specific_Competency__pk=self.indikator,
                                           grade=1).count()
        totalscore = (float(score) / float(allquestion)) *100
        totalscore = (round(totalscore, 0))

        return totalscore, allquestion

    def keberadaanIndikator(self):

        sc = ScoreDetil.objects.filter(quiz_taker = self.quiz_taker).values_list('specific_competency', flat=True)
        nextInd = Specific_Competency.objects.filter(base_Competency=self.question.specific_Competency.base_Competency.pk).exclude(pk__in=sc)
        nextInd = nextInd.filter(roll_out = 1)
        if nextInd.exists():
            nextInd = nextInd.order_by('order').first()

        return nextInd


    def menghitungIndikator(self):
        # indikatorexist = Base_Competency.objects.filter(pk=self.question.specific_Competency.base_Competency.pk)
        # indikator_yang_belum = self.keberadaanIndikator()
        # ordernext = indikator_yang_belum.order

        sc = ScoreDetil.objects.filter(quiz_taker = self.quiz_taker).values_list('specific_competency', flat=True)
        nextInd = Specific_Competency.objects.filter(base_Competency=self.question.specific_Competency.base_Competency.pk,roll_out = 1).exclude(pk__in=sc)
        if nextInd.exists():
            nextInd = nextInd.order_by('order').first()
            ordernext = nextInd.order
        else :
            ordernext = 0

        indikatorexist = Base_Competency.objects.filter(pk=self.question.specific_Competency.base_Competency.pk,
                                                        k_dasar__order=ordernext)

        return indikatorexist, ordernext


    def menghitungIndikator2(self):
        indikatornow = self.question.specific_Competency.order
        indikatornext = int(indikatornow) + 1
        ordernext = int(indikatornext)
        indikatorexist = Base_Competency.objects.filter(pk=self.question.specific_Competency.base_Competency.pk,
                                                        k_dasar__order=ordernext)
        return indikatorexist, ordernext

    def menghitungScoreKeseluruhan(self):
        scoreDetails = ScoreDetil.objects.filter(quiz_taker_id=self.quiz_taker).aggregate(Avg('desc'))['desc__avg']
        return float(scoreDetails)


class PemilihanKemampuan:
    def __init__(self,quiz,student):
        self.quiz = quiz
        self.student = student

    def soalKemampuan(self, Hasil):
        satuindikator = self.student.user.get_unanswered_questions(self.quiz)
        # verylow
        if Hasil < -0.5:
            satuindikator = satuindikator.filter(level__lte=0)
            var = "verylow"
        # Low
        elif Hasil > -1 and Hasil < 0.5:
            satuindikator = satuindikator.filter(level__lte=0)
            var = "low"

        # Averange
        elif Hasil > 0 and Hasil < 1.5:
            satuindikator = satuindikator.filter(level__lte=2, level__gte=-1)
            var = "Averange"

        # good
        elif Hasil > 0.5 and Hasil < 2:
            satuindikator = satuindikator.filter(level__gte=1)
            var = "good"

        # excellent
        elif Hasil > 1.5:
            satuindikator = satuindikator.filter(level__gte=1)
            var = "excelent"

        return satuindikator, var

    def soalKemampuan2(self,Hasil):
        satuindikator = self.student.user.get_unanswered_questions(self.quiz)
        # verylow
        if Hasil < -0.5:
            satuindikator = satuindikator.filter(level__lte=-1, level__gte=-3)
            var = "verylow"
        # Low
        elif Hasil > -1 and Hasil < 0.5:
            satuindikator = satuindikator.filter(level__lte=0, level__gte=-1)
            var = "low"

        # Averange
        elif Hasil > 0 and Hasil < 1.5:
            satuindikator = satuindikator.filter(level__lte=1, level__gte=0)
            var = "Averange"

        # good
        elif Hasil > 0.5 and Hasil < 2:
            satuindikator = satuindikator.filter(level__lte=2, level__gte=1)
            var = "good"

        # excellent
        elif Hasil > 1.5:
            satuindikator = satuindikator.filter(level__gte=2)
            var = "excelent"

        return satuindikator, var



