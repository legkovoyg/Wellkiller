from django import forms
from django.contrib.auth import get_user_model

class LoginUserForm(forms.Form):
    username = forms.CharField(label = "",
                               widget = forms.TextInput(attrs = {'class':"loginPass", "placeholder":"Логин" }))
    password = forms.CharField(label = "",
                               widget = forms.PasswordInput(attrs = {'class':"loginPass password", "placeholder":"Пароль"}))


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label = "", widget = forms.TextInput(attrs = {'class':"input","placeholder":"Введите свой логин"}))
    email = forms.EmailField(label="", widget = forms.EmailInput(attrs = {'class':"input","placeholder":"Введите свою почту"}))
    first_name = forms.CharField(label = '', widget= forms.TextInput(attrs = {'class':"input","placeholder":"Введите свое имя"}))
    last_name = forms.CharField(label = '', widget= forms.TextInput(attrs = {'class':"input","placeholder":"Введите свою фамилию"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs = {'class':"input", "placeholder":"Введите свой пароль"}))
    password_2 = forms.CharField(label="", widget=forms.PasswordInput(attrs = {'class':"input", "placeholder":"Введите свой пароль еще раз "}))
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name','password', 'password_2']
        labels = {
            'email': 'E-mail',
            'first_name':'Имя',
            'last_name':'Фамилия',
        }

    def clean_password_2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_2']:
            raise forms.ValidationError("Пароли не совпадают")
        return cd['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email = email).exists():
            raise forms.ValidationError("Такой email уже существует!")
        return email


