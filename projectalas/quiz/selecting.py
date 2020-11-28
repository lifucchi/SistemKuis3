from .models import Topic,Base_Competency,ScoreDetil,Core_Competency,Specific_Competency, Question, Answer, QuizTaker, UsersAnswer , Subject, QuizLog

from . import fuzzy


class Menghitung:

    def __init__(self ,quiz_taker, quiz, indikator):
        # self.question = question
        self.quiz_taker = quiz_taker
        self.indikator = indikator
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
                                                 question__specific_Competency__pk=self.indikator).count()
        score = UsersAnswer.objects.filter(quiztaker_id=self.quiz_taker, question__specific_Competency__pk=self.indikator,
                                           grade=1).count()
        totalscore = float(score) / float(allquestion)
        return totalscore, allquestion

    # def menghitungIndikator(self):
    #     indikatornow = self.question.specific_Competency.order
    #     indikatornext = int(indikatornow) + 1
    #     ordernext = int(indikatornext)
    #     indikatorexist = Base_Competency.objects.filter(pk=self.question.specific_Competency.base_Competency.pk,
    #                                                     k_dasar__order=ordernext)
    #     return indikatorexist, ordernext
    #

    #
    # def menghitungScoreKeseluruhan(self):
    #     scoreDetails = ScoreDetil.objects.filter(quiz_taker_id=self.quiz_taker).aggregate(Avg('desc'))['desc__avg']
    #     return float(scoreDetails)



class PemilihanKemampuan:
    def __init__(self, Hasil, quiz,student):
        self.Hasil = Hasil
        self.quiz = quiz
        self.student = student

    def soalKemampuan(self):
        satuindikator = self.student.user.get_unanswered_questions(self.quiz)
        # verylow
        if self.Hasil < -0.5:
            satuindikator = satuindikator.filter(level__lte=-1, level__gte=-3)
            var = "verylow"
        # Low
        elif self.Hasil > -1 and self.Hasil < 0.5:
            satuindikator = satuindikator.filter(level__lte=0, level__gte=-1)
            var = "low"

        # Averange
        elif self.Hasil > 0 and self.Hasil < 1.5:
            satuindikator = satuindikator.filter(level__lte=1, level__gte=0)
            var = "Averange"

        # good
        elif self.Hasil > 0.5 and self.Hasil < 2:
            satuindikator = satuindikator.filter(level__lte=2, level__gte=1)
            var = "good"

        # excellent
        elif self.Hasil > 1.5:
            satuindikator = satuindikator.filter(level__gte=2)
            var = "excelent"

        return satuindikator, var



