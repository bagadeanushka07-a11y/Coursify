from django import forms
from accounts.models import User


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile_picture",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-input"
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "First name"
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Last name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Email address"
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Phone number"
                }
            ),

            "profile_picture": forms.ClearableFileInput(
                attrs={
                    "class": "form-input"
                }
            ),
        }