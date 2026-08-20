
from django import forms

from .models import Lesson


class LessonForm(forms.ModelForm):

    class Meta:

        model = Lesson

        fields = [
            "title",
            "description",
            "video_url",
            "order",
            "duration",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter lesson title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "placeholder": "Describe this lesson",
                    "rows": 5
                }
            ),

            "video_url": forms.URLInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "https://www.youtube.com/..."
                }
            ),

            "order": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Lesson number",
                    "min": 1
                }
            ),

            "duration": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Duration in minutes",
                    "min": 0
                }
            ),
        }

