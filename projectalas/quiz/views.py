from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import  HttpResponse , request , response
# from django.views.generic import TemplateView
from django.views.generic import DetailView, ListView , View
# from quiz.serializers import QuizListSerializer, QuizDetailSerializer, UsersAnswerSerializer, QuizResultSerializer
from .models import Topic,Base_Competency,Core_Competency,Specific_Competency, Question, Answer, QuizTaker, UsersAnswer , Subject
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.db import transaction

from .forms import ChooseAnswerForm

class topicList (ListView):
    model = Topic
    # queryset = Question.objects.all()
    template_name = 'quiz/class-page.php'
    context_object_name = 'topic_list'

    def get_queryset(self):
        queryset = super(topicList, self).get_queryset()
        return queryset

@login_required()
def topicDetail (request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    bc = Base_Competency.objects.filter(topic=topic)
    return render(request, 'quiz/class-topic-page.php', {
        'topics': topic,
        'bcs': bc})


@login_required
def take_quiz(request, pk):

    quiz = get_object_or_404(Specific_Competency, pk=pk)
    student = request.user
    obj = QuizTaker.objects.create(user=student, specific_competency=quiz)
    quiz_taker = obj.pk

    if student.get_unanswered_questions(quiz).exists():
        unanswered_questions = student.get_unanswered_questions(quiz)
        question = unanswered_questions.filter(level__lte = 0.7)
        question = question.filter(level__gte = 0.3)
        question = question.first()

        # return redirect('question', question_id=question.id )
        # return redirect('question', question_id=question.id)
        return redirect('question' , quiz = quiz.pk, quiz_taker = quiz_taker, question_id=question.id)
    else:
        question = quiz.indikator.order_by('?')
        question = question.first()
        return redirect('question' , quiz = quiz.pk, quiz_taker = quiz_taker, question_id=question.id)

    # quiz = Quiz.objects.get(pk=quiz_id)
    # just get first question in quiz for now
    # question = Question.objects.get(pk=question_id)
    # unanswered_questions = student.get_unanswered_questions(quiz)
    # question = unanswered_questions.first()
    # answers = question.choices.all().order_by('label')

    # could simulate web service request to get: questions, answers
    # question_data = requests.get(reverse('adaptive_engine:get_question'),params={'id':question.id})
    # question_text = question_data['text']

    # alternative: get objects directly
    # choose_answer_form = ChooseAnswerForm()
    # choose_answer_form.fields['answer'].queryset = answers
    #
    # context = {
    #     'question': question,
    #     'form': choose_answer_form,
    # }
    #
    # return render(request, 'quiz/take_quiz_form.php', context)

def question(request,quiz,quiz_taker,question_id):
    student = QuizTaker.objects.get(pk=quiz_taker)
    question = Question.objects.get(pk=question_id)
    quiz = get_object_or_404(Specific_Competency, pk=quiz)

    if request.method == 'GET':
        question = Question.objects.get(pk=question_id)
        student = QuizTaker.objects.get(pk=quiz_taker)
        answered_questions = student.quiz_answers.count()

        # answers = question.choices.all().order_by('?')
        answers = question.choices.all().order_by('?')

        choose_answer_form = ChooseAnswerForm()
        choose_answer_form.fields['answer'].queryset = answers

        context = {
                'question':question,
                'form': choose_answer_form,
                'answered_questions': answered_questions,
                # 'quiztaker' : student

            }

        return render(request, 'quiz/take_quiz_form.php', context)

    elif request.method == 'POST':
        choose_answer_form = ChooseAnswerForm(request.POST)
        if choose_answer_form.is_valid():
            answer = choose_answer_form.cleaned_data['answer']

            if answer.is_correct:
                grade = 1
            else:
                grade = 0

            response = UsersAnswer(
                quiztaker=student,
                question=question,
                answer=answer,
                grade=grade,
            )
            response.save()

            # score = UsersAnswer.objects.filter(quiztaker = quiz_taker).filter(answer__is_correct = 1),count()
            # score = UsersAnswer.objects.filter(quiztaker = quiz_taker)
            score = UsersAnswer.objects.filter(grade = 1).count()
            # score = UsersAnswer.grade.count()

            QuizTaker.objects.filter(pk=quiz_taker).update(score=score)

            # response = UsersAnswer(
            #     quiztaker=student,
            #     question=question,
            #     answer=answer,
            #     # grade=grade,
            # )

            #fuzzynya disini harusnya
            answered_questions = student.quiz_answers.count()

            if answered_questions % 5 == 0:
                # hitung fuzzy

                return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=question.id)

            else:
                if student.user.get_unanswered_questions(quiz).exists():
                    unanswered_questions = student.user.get_unanswered_questions(quiz)
                    question = unanswered_questions.first()
                else:
                    question = quiz.indikator.order_by('?')
                    question = question.first()

                return redirect('question', quiz=quiz.pk, quiz_taker=student.pk, question_id=question.id)

            # return render(request, 'quiz/take_quiz_form.php', context)

            # question =
            #
            # context = {
            #     'question': question,
            #     'form': choose_answer_form,
            #     # 'quiztaker' : student
            #
            # }
            #
            # return render(request, 'quiz/take_quiz_form.php', context)

            #sepertinya fuzzynya disini terus bikin question lagi

    # quiz = get_object_or_404(Specific_Competency, pk=pk)
    # student = request.user
    #
    # total_questions = quiz.indikator.count()
    #
    # unanswered_questions = student.get_unanswered_questions(quiz)
    # total_unanswered_questions = unanswered_questions.count()
    # progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    # question = unanswered_questions.first()
    #
    # if request.method == 'POST':
    #     # form = TakeQuizForm(question=question, data=request.POST)
    #     form = TakeQuizForm(question=question, data=request.POST)
    #
    #     if form.is_valid():
    #         with transaction.atomic():
    #             student_answer = form.save(commit=False)
    #             quiz_taker = get_object_or_404(QuizTaker, pk=student.id)
    #
    #             student_answer.quiztaker  = quiz_taker.pk
    #             student_answer.question = question.pk
    #             student_answer.save()
    #
    #             # return redirect('topic')
    #
    # else:
    #     # QuizTaker.objects.create(user=student, specific_competency=quiz)
    #     # obj = QuizTaker.objects.get_or_create(user = student, specific_competency = quiz)
    #     # UsersAnswer.objects.create(quiztaker = obj, question = question)?
    #     form = TakeQuizForm(question=question)
    #     # total_questions = quiz.indikator.count()
    #
    # return render(request, 'quiz/take_quiz_form.php', {
    #     'quiz': quiz,
    #     'question': question,
    #     'form': form,
    #     'progress': progress,
    #     'answered_questions': total_questions - total_unanswered_questions,
    #     'total_questions': total_questions
    # })




# Create your views here.
# class topicList(ListView):
#     model = Specific_Competency
#     ordering = ('name', )
#     context_object_name = 'indikator'
#     template_name = 'classroom/students/quiz_list.html'
#
#     def get_queryset(self):
#         student = self.request.user.student
#         # student_interests = student.interests.values_list('pk', flat=True)
#         taken_quizzes = student.quizzes.values_list('pk', flat=True)
#         queryset = Quiz.objects.exclude(pk__in=taken_quizzes) \
#             .annotate(questions_count=Count('questions')) \
#             .filter(questions_count__gt=0)
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['student_subjects'] = self.request.user.student.interests.values_list('pk', flat=True)
#         return context