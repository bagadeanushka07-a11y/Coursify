
from django import forms

from .models import Quiz, Question


class QuizForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = [
            "course",
            "title",
            "description",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter quiz title"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter quiz description",
                    "rows": 4
                }
            ),
        }


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = [
            "question_text",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_answer",
        ]

        widgets = {
            "question_text": forms.TextInput(
                attrs={
                    "placeholder": "Enter question"
                }
            ),
            "option_a": forms.TextInput(
                attrs={
                    "placeholder": "Option A"
                }
            ),
            "option_b": forms.TextInput(
                attrs={
                    "placeholder": "Option B"
                }
            ),
            "option_c": forms.TextInput(
                attrs={
                    "placeholder": "Option C"
                }
            ),
            "option_d": forms.TextInput(
                attrs={
                    "placeholder": "Option D"
                }
            ),
        }