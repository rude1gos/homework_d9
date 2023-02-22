from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author', 'category', 'header_post', 'text_post'
        ]

    def clean(self):
        cleaned_data = super().clean()
        header_post = cleaned_data.get('header_post')
        text_post = cleaned_data.get('text_post')

        if text_post is not None and header_post == text_post:
            raise ValidationError(
                "Текст статьи не должен быть идентичен заголовку статьи"
            )
        return cleaned_data