from django import forms

class SignUpForm(forms.Form):
    tenant_name = forms.CharField(max_length = 150)
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput, min_length=8)

class SignInForm(forms.Form):
    tenant_name = forms.CharField(max_length = 150)
    password = forms.CharField(widget = forms.PasswordInput, min_length=8)
