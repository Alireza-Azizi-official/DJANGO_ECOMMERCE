from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact, Comment
from django import forms


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, help_text='eg. youremail@gmail.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')


class Contact(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        
        
class SearchBox(forms.Form):
    query = forms.CharField(max_length=100, required=False, label = 'Search Products')
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows':4, 'placeholder':'اینجا کامنت خود را بنویسید....'}),
        }

