from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from info.models import UserProfile
from django.forms import ModelForm

AGE = ([18,18],[19,19],[20,20],[21,21],[22,22],[23,23],[24,24])
class RegistrationForm(ModelForm):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
    label='Password (Again)',
    widget=forms.PasswordInput()
    )
    age = forms.ChoiceField(
        label='Age',
        choices=AGE
    )
    class Meta:
        model = UserProfile
        exclude = ('user')


    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if not re.search(r'^\w+$',username):
            raise forms.ValidationError('Wrong spellings')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')

class EditProfileForm(forms.Form):
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={'size': 128})
    )
    age = forms.ChoiceField(
        label='Age',
        choices=AGE
    )

    university = forms.CharField(
        label='University',
        widget=forms.TextInput(attrs={'size': 50})
    )
    home_city = forms.CharField(
        label='Home City',
        widget=forms.TextInput(attrs={'size': 50})
    )
    away_city = forms.CharField(
        label='Destination City',
        widget=forms.TextInput(attrs={'size': 50})
    )

TYPE_INTEREST = (['Music','Music'],['Sports','Sports'],['Movie','Movie'],['Game','Game'])
class InterestSaveForm(forms.Form):
    type_interest = forms.ChoiceField(
        label='Type of interest',
        widget=forms.Select(),choices=TYPE_INTEREST
    )
    description = forms.CharField(
        label='Description',
        widget=forms.TextInput(attrs={'size': 128})
    )
    tags = forms.CharField(
        label='Tags',
        required=False,
        widget=forms.TextInput(attrs={'size': 64})
    )
