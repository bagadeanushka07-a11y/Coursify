from django import forms
from .models import Course


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course

        fields = [
            "title",
            "description",
            "category",
            "price",
            "level",
            "duration",
            "thumbnail",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter course title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "placeholder": "Describe your course",
                    "rows": 5
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-input"
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter course price",
                    "step": "0.01"
                }
            ),

            "level": forms.Select(
                attrs={
                    "class": "form-input"
                }
            ),

            "duration": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Duration in hours"
                }
            ),

            "thumbnail": forms.ClearableFileInput(
                attrs={
                    "class": "form-input"
                }
            ),
        }