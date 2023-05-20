from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User

from shop_mag.models import ContactRequest


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please enter your user name"}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter your first name"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please enter your last name"}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter your email address"}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': "Please enter your password"})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': "Please enter your password"})


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter your first name"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please enter your last name"}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter your email address"}),
        }


class UserResetPassword(PasswordResetForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Please enter your email address"})
        }


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})