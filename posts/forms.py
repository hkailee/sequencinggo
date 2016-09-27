from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'tags')

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    From = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class SearchForm(forms.Form):
    query = forms.CharField()

