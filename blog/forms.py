from django import forms
from .models import Comment_djb

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment_djb
        fields = ('name', 'email', 'body')

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=True, widget=forms.Textarea)