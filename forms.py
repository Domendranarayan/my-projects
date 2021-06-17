from .models import  Post
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput (attrs={'placeholder':'Password'}))
    password2 = forms.CharField(label='Re-Enter', widget=forms.PasswordInput (attrs={'placeholder':'Re-Enter Password'}))
    class Meta:
        model = User
        fields = ('username', 'email')
        help_texts = {'username': None}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

# class CommentForm(forms.ModelForm):
#     class Meta():
#         model    = Comment
#         fields   = ('body',)
#         widgets  = {
#             'body':forms.Textarea(attrs={'class':'editable medium-editor-textarea '})

#         }

class  PostForm(forms.ModelForm):
    class Meta:
        model= Post
        fields = ('title', 'author', 'content', 'image', 'publish', 'status')
        widgets = {
            'title'  : forms.TextInput(attrs={'class':'form-control'}),
            'author' : forms.TextInput(attrs={'class':'form-control' , 'value': '', 'id':'elder', 'type':'hidden' }),
            'content': forms.Textarea(attrs={'class':'form-control' })
        }

class SearchForm(forms.Form):
    query = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs.update({'class': 'form-control '})