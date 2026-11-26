
from django import forms
from .models import Post


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            return [
                single_file_clean(file, initial)
                for file in data
            ]

        return single_file_clean(data, initial)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['caption']
        widgets = {
            'caption': forms.Textarea(attrs={
                'placeholder': 'What is happening in your universe?',
                'maxlength': 150,
                'rows': 3,
            })
        }


class PostMediaForm(forms.Form):
    files = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'multiple': True,
            'accept': 'image/*,video/*'
        })
    )
