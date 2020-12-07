from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.conf import settings


# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Mata Pelajaran'
        verbose_name_plural = "Mata Pelajaran"

    def natural_key(self):
        return self.name


class Core_Competency(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="mapel")
    name = models.CharField(max_length=400)
    desc = models.CharField(max_length=100)
    classes = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Kompetensi Inti"
        verbose_name_plural = "Kompetensi Inti"


    def __str__(self):
        return self.classes

    def natural_key(self):
        return self.classes

class Topic(models.Model):
    name = models.CharField(max_length=400)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = "Topik"
        verbose_name_plural = "Topik"

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name

class Base_Competency(models.Model):
    core_Competency = models.ForeignKey(Core_Competency, on_delete=models.CASCADE, related_name="k_inti")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topictopic")
    roll_out = models.BooleanField(default=False)
    name = models.CharField(max_length=400)
    ability = models.CharField(max_length=100, blank = True)

    class Meta:
        verbose_name = "Kompetensi Dasar"
        verbose_name_plural = "Kompetensi Dasar"

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name

class Specific_Competency(models.Model):
    base_Competency = models.ForeignKey(Base_Competency, on_delete=models.CASCADE , related_name="k_dasar")
    name = models.CharField(max_length=400)
    description = models.CharField(max_length=70,blank=True)
    order = models.IntegerField(default=0)
    roll_out = models.BooleanField(default=False)

    # timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Indikator"
        verbose_name_plural = "Indikator"

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name

class Question(models.Model):
    specific_Competency = models.ForeignKey(Specific_Competency, on_delete=models.CASCADE, related_name="indikator")
    label = models.CharField(max_length=200)
    level = models.FloatField(default=0)
    discrimination = models.FloatField(default=0)
    code = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Pertanyaan"
        verbose_name_plural = "Pertanyaan"

    def natural_key(self):
        return self.name

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    label = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Jawaban Pertanyaan"
        verbose_name_plural = "Jawaban Pertanyaan"

    def natural_key(self):
        return self.label

class QuizTaker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name="murid")
    score = models.FloatField(default=0)
    completed = models.BooleanField(default=False)
    date_finished = models.DateTimeField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    recommendation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Pengambil Kuis"
        verbose_name_plural = "Pengambil Kuis"


    def natural_key(self):
        return self.user.username

class ScoreDetil(models.Model):
    specific_competency = models.ForeignKey(Specific_Competency, on_delete=models.CASCADE , related_name="indikators")
    quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE , related_name="quiz_taker")
    desc = models.CharField(max_length=200)
    # question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    # label = models.CharField(max_length=200)
    # is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.desc

    class Meta:
        verbose_name = "Skor per Indikator"
        verbose_name_plural = "Skor per Indikator"

    def natural_key(self):
        return self.desc


class UsersAnswer(models.Model):
    quiztaker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE, related_name="quiz_answers")
    # question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='+')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, related_name='+')
    timestamp = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Jawaban Pengguna"
        verbose_name_plural = "Jawaban Pengguna"

    def __str__(self):
        return self.question.label

    def natural_key(self):
        return self.question.label


class QuizLog(models.Model):
    quiztaker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE, related_name="person_answers")
    questionlog = models.IntegerField(default=0)
    sclog = models.IntegerField(default=0)
    ql_a = models.FloatField(default=0)
    ql_b = models.FloatField(default=0)
    ql_p = models.FloatField(default=0)
    ql_c = models.FloatField(default=0)
    ql_r = models.FloatField(default=0)
    ql_ability = models.FloatField(default=0)
    ql_deltaability = models.FloatField(default=0)


    def __str__(self):
        return self.QuizLog.label

    def natural_key(self):
        return self.QuizLog.label


@receiver(pre_save, sender=Topic)
def slugify_name(sender, instance, *args, **kwargs):
    instance.slugs = slugify(instance.name)