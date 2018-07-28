from django import forms

class LoginForm(forms.Form):
    uname = forms.CharField(label='Username', max_length=100,)
    pwd = forms.CharField(label='Password', max_length=256)