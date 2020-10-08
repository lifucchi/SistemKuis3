from django.urls import path, re_path
# from quiz.api import QuizListAPI, QuizDetailAPI, MyQuizListAPI, SaveUsersAnswer, SubmitQuizAPI
from django.conf.urls import url
from .views import topicList
from . import views

urlpatterns = [
    path(r"", topicList.as_view(), name='topic'),
    re_path(r"^(?P<slug>[\w\-]+)/$", views.topicDetail, name='topicDetail'),
    path('quiz/<int:pk>/', views.take_quiz, name='take_quiz'),
    re_path(r'^quiz/(?P<quiz>[0-9]+)/(?P<quiz_taker>[0-9]+)/(?P<question_id>[0-9]+)/$', views.question, name='question'),

]
