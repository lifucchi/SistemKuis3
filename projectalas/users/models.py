from django.db import models

# Create your models here.
from users.managers import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from quiz.models import *


class User(AbstractBaseUser, PermissionsMixin):
    # name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'), unique=True)
    username = models.CharField(_('username'), unique=True, max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(_('nama depan'), max_length=100)
    last_name = models.CharField(_('nama belakang'), max_length=100)
    classes = models.CharField(_('kelas'), max_length=100 , blank=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','last_name','email']

    objects = CustomUserManager()

    def get_unanswered_questions(self, quiz):
        answered_questions = self.murid \
            .filter(quiz_answers__question__specific_Competency=quiz) \
            .values_list('quiz_answers__question__id', flat=True)
        questions = quiz.indikator.exclude(pk__in=answered_questions)
        return questions


    def __str__(self):
        return self.username