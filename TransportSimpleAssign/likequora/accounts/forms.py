from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(UserLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        username = data['username']
        password = data['password']

        user = authenticate(request, username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid credentials")
        return data


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        # username_status = bool(User.objects.get(username=username))
        # email_status = bool(User.objects.get(email=email))

        if password != confirm_password:
            raise forms.ValidationError('Password not Matching')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        username_status = bool(User.objects.filter(username=username))
        if username_status:
            raise forms.ValidationError('username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        email_status = bool(User.objects.filter(email=email))
        if email_status:
            raise forms.ValidationError('email already exists')
        return email
