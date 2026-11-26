
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose your username'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'avatar',
            'bio',
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Your hero name'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email address'
            }),

            'bio': forms.Textarea(attrs={
                'placeholder': 'Tell your story...',
                'maxlength': 160,
                'rows': 4,
            }),
        }
