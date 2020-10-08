from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.conf import settings


# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name


class Core_Competency(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="mapel")
    name = models.CharField(max_length=400)
    desc = models.CharField(max_length=100)
    classes = models.CharField(max_length=100)

    def __str__(self):
        return self.classes

    def natural_key(self):
        return self.classes

class Topic(models.Model):
    name = models.CharField(max_length=400)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name

class Base_Competency(models.Model):
    core_Competency = models.ForeignKey(Core_Competency, on_delete=models.CASCADE, related_name="k_inti")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topictopic")

    name = models.CharField(max_length=400)
    ability = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name

class Specific_Competency(models.Model):
    base_Competency = models.ForeignKey(Base_Competency, on_delete=models.CASCADE , related_name="k_dasar")
    name = models.CharField(max_length=400)
    description = models.CharField(max_length=70)
    # image = models.ImageField()
    # slug = models.SlugField(blank=True)
    roll_out = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp',]
        verbose_name_plural = "Specific_Competencies"

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name

class Question(models.Model):
    # specific_Competency = models.ForeignKey(Specific_Competency, on_delete=models.CASCADE)
    # specific_Competency = models.ManyToManyField(Specific_Competency)
    # specific_Competency = models.ManyToManyField(Specific_Competency, through= question)
    specific_Competency = models.ForeignKey(Specific_Competency, on_delete=models.CASCADE, related_name="indikator")
    label = models.CharField(max_length=200)
    level = models.FloatField(default=0)
    discrimination = models.FloatField(default=0)
    # c_prob = models.FloatField(default=0)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.label

    def natural_key(self):
        return self.name

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    label = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    def natural_key(self):
        return self.label

class QuizTaker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name="murid")
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    specific_competency = models.ForeignKey(Specific_Competency, on_delete=models.CASCADE , related_name="indikator_diambil")
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    date_finished = models.DateTimeField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    recommendation = models.CharField(max_length=100)

    # def get_unanswered_questions(self, quiz):
    #     answered_questions = self.quiz_answers \
    #         .filter(question__specific_Competency=quiz) \
    #         .values_list('question__id ', flat=True)
    #     questions = quiz.indikator.exclude(pk__in=answered_questions).order_by('label')
    #     return questions

    def __str__(self):
        return self.user.username


    def natural_key(self):
        return self.user.username


class UsersAnswer(models.Model):
    quiztaker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE, related_name="quiz_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='+')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, related_name='+')
    timestamp = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(default=0)
    def __str__(self):
        return self.question.label

    def natural_key(self):
        return self.question.label


class QuizLog(models.Model):
    quiztaker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE, related_name="person_answers")
    # ql_a = models.FloatField(default=0)
    # ql_b = models.FloatField(default=0)
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