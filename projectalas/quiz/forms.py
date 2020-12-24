from django import forms
from django.forms import ModelChoiceField, Form
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from random import shuffle
from .models import Topic,Base_Competency,Core_Competency,Specific_Competency, Question, Answer, QuizTaker, UsersAnswer , Subject


class ChooseAnswerForm(forms.Form):
    '''
    Quiz form 1: Student chooses answer to question
    On initialization (in view), restrict the answer queryset to specific question's answer choices
    '''
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.all(),
        widget=forms.RadioSelect,
        empty_label=None,
        blank=False,
    )

    # def clean(self):
    #     cleaned_data = super(ChooseAnswerForm, self).clean()
    #     t = self.cleaned_data.get('answer')
    #     if t == '':
    #         raise forms.ValidationError('tolong diisi')
    #     return cleaned_data
    #
    # class Meta:
    #     model = UsersAnswer
    #     fields = ('answer', )


class QuizTakerForm(forms.ModelForm):
    class Meta:
        model = QuizTaker
        fields = ('user',)


# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ('label', )
#
# class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
#     def clean(self):
#         super().clean()
#
#         has_one_correct_answer = False
#         for form in self.forms:
#             if not form.cleaned_data.get('DELETE', False):
#                 if form.cleaned_data.get('is_correct', False):
#                     has_one_correct_answer = True
#                     break
#         if not has_one_correct_answer:
#             raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')
#
# class TakeQuizForm(forms.ModelForm):
#     answer = forms.ModelChoiceField(
#         queryset=Answer.objects.none(),
#         widget=forms.RadioSelect(),
#         to_field_name='pk',
#         disabled=False,
#         required=True,
#         empty_label=None)
#
#     class Meta:
#         model = UsersAnswer
#         fields = ('answer', )
#
#     def __init__(self, *args, **kwargs):
#         question = kwargs.pop('question')
#         super().__init__(*args, **kwargs)
#         self.fields['answer'].queryset = question.choices.order_by('?')
#         # self.fields['id'].queryset = question.choices.order_by()
#
#         # Get did queryset for the selected fid
#         if 'id' in self.data:
#             try:
#                 fid = int(self.data.get('id'))
#                 self.fields['id'].queryset = question.choices.filter(
#                     id=fid).order_by()
#             except (ValueError, TypeError):
#                 # invalid input from the client; ignore and use empty queryset
#                 pass
#
#     # def get_initial(self):
#     #     """
#     #     Returns the initial data to use for forms on this view.
#     #     """
#     #     initial = super(TakeQuizForm, self).get_initial()
#     #     if self.answer is not None:
#     #         initial['answer'] = Model.objects.get(pk=self.answer)
#     #     return initial
