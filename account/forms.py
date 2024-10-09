from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from account.models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=100, label='کلمه عبور')
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=100, label='تکرار کلمه عبور')

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("کلمه عبور با تکرار آن مغایرت دارد")
        return cd['password2']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'phone_number','password')
