from os import name
from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name=forms.CharField(max_length=25,label="Name")
    email=forms.EmailField(label="Email")
    to=forms.EmailField(label="Send To")
    comments=forms.CharField(label="Comments",required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')
class SearchForm(forms.Form):
    query =forms.CharField()
