from django.urls import path, re_path
# from quiz.api import QuizListAPI, QuizDetailAPI, MyQuizListAPI, SaveUsersAnswer, SubmitQuizAPI
from django.conf.urls import url
from .views import TopicList , SubjectsList, ClassList, ScoresList,ScoreList
from . import views

urlpatterns = [
    path(r"", SubjectsList.as_view(), name='subjects'),
    path(r"kelas/<int:pk>/", ClassList.as_view(), name='classes'),
    path(r"kelas/topik/<int:pk>/", TopicList.as_view(), name='topics'),
    path(r"kelas/nilai/<int:pk>/", ScoresList.as_view(), name='scores'),
    path(r"kelas/topik/nilai/<int:pk>/<int:bc>/", ScoreList.as_view(), name='score'),
    # re_path(r"^(?P<slug>[\w\-]+)/$", views.topicDetail, name='topicDetail'),
    # path('<slug:slug>/', views.TopicDetailView.as_view(), name='topicDetail'),
    path('quiz/<int:pk>/', views.take_quiz, name='take_quiz'),
    # path('quiz/<int:pk>/', views.TakeQuiz.as_view(), name='take_quiz'),

    re_path(r'^quiz/(?P<quiz>[0-9]+)/(?P<quiz_taker>[0-9]+)/(?P<question_id>[0-9]+)/$', views.question, name='question'),

]
