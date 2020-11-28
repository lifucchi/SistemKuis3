
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



