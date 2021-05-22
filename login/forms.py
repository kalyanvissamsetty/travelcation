from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from .models import Profile


class CreateUserForm(ModelForm):
    phone = forms.CharField()

    class Meta:
        USERNAME_FIELD = 'email'
        model = User
        fields = ['username', 'email', 'phone', 'password']



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,13}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed.")
    phone = forms.CharField(validators=[phone_regex], max_length=17)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = False
        for field in UserRegisterForm.Meta.fields:
            self.fields[field].label = False
            self.fields[field].help_text = None

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        if User.objects.filter(email=email):
            raise forms.ValidationError('Email already exists.')
        if User.objects.filter(username=username):
            raise forms.ValidationError('Username already exists.')
        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{10,13}$',
    #                              message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed.")
    # phone = forms.CharField(validators=[phone_regex], max_length=17)

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']



