from django import forms

class LoginUserForm(forms.Form):
    username = forms.CharField(label = "",
                               widget = forms.TextInput(attrs = {'class':"loginPass", "placeholder":"Логин" }))
    password = forms.CharField(label = "",
                               widget = forms.PasswordInput(attrs = {'class':"loginPass password", "placeholder":"Пароль"}))