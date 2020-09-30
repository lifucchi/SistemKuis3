from django.urls import path, re_path
# from quiz.api import QuizListAPI, QuizDetailAPI, MyQuizListAPI, SaveUsersAnswer, SubmitQuizAPI
from django.conf.urls import url
from .views import topicList
from . import views

urlpatterns = [
    # path("my-quizzes/", MyQuizListAPI.as_view()),
    # path(r"quizzes/", QuizListAPI.as_view()),
    # path(r"quizzes/", QuizList.as_view()),
    # path('home/', home, name='home'),
    path(r"", topicList.as_view(), name='topic'),
    re_path(r"^(?P<slug>[\w\-]+)/$", views.topicDetail, name='topicDetail'),
    path('quiz/<int:pk>/', views.take_quiz, name='take_quiz'),
    # re_path(r'^question/(?P<question_id>[0-9]+)$', views.question, name='question'),
    re_path(r'^quiz/(?P<quiz>[0-9]+)/(?P<quiz_taker>[0-9]+)/(?P<question_id>[0-9]+)/$', views.question, name='question'),
    # re_path(r'^quiz/<int:pk>/(?P<quiz_taker>[0-9]+)/(?P<question_id>[0-9]+)/$', views.question, name='question'),

    # re_path(r'^question/(?P<question_id>[0-9]+)/(?P<quiz_taker>[0-9]+)$', views.question, name='question'),

    # re_path(r"^(?P<slug>[\w\-]+)/take/<int:pk>/$", views.topicDetail, name='topicDetail'),

    #     path("quizzes/", MyQuizList.as_view()),
#
#     url(r'^api/quizzes/$', QuizListAPI.as_view()),
#     url(r'^api/quizzes/(?P<pk>[0-9]+)/$', api.QuizDetail.as_view()),
#     url(r'^quizzes/', QuizListAPI.as_view()),
#     path("save-answer/", SaveUsersAnswer.as_view()),
#     re_path(r"quizzes/(?P<slug>[\w\-]+)/submit/$", SubmitQuizAPI.as_view()),
]
