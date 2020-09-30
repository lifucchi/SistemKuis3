from django.contrib import admin

# Register your models here.
from django.contrib import admin
import nested_admin
from .models import Topic,Base_Competency,Core_Competency,Specific_Competency, Question, Answer, QuizTaker, UsersAnswer , Subject


class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 4
    max_num = 4


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [AnswerInline,]
    extra = 5


# class IndikatorInline(nested_admin.NestedTabularInline):
#     model = Specific_Competency
#     inlines = [QuestionInline,]
#     extra = 5


# class Question_DetailInLine(nested_admin.NestedTabularInline):
#     model = Question_Detail
#     extra = 1

# class QuestionAdmin(nested_admin.NestedModelAdmin):
#     inlines = [, AnswerInline,]

# class ScAdmin(nested_admin.NestedModelAdmin):
#     inlines = [,]

class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline,]

#
# class QuestionAdmin(admin.ModelAdmin):
#     inlines = [QuestionInline,]


class UsersAnswerInline(admin.TabularInline):
    model = UsersAnswer


class QuizTakerAdmin(admin.ModelAdmin):
    inlines = [UsersAnswerInline,]

# class Core_Competency(nested_admin.NestedTabularInline):
#     model = Core_Competency
#     extra = 5

admin.site.register(Specific_Competency, QuizAdmin)
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Question_Detail)

# admin.site.register(QuizAdmin)
# admin.site.register(Question,QuizAdmin)
admin.site.register(Core_Competency)
admin.site.register(Base_Competency)
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizTaker, QuizTakerAdmin)
admin.site.register(UsersAnswer)
admin.site.register(Subject)