from .models import Comment, Post
from django import forms
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))
    class Meta:
        model = Post
        fields = ('title', 'date_posted', 'content', 'author',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')