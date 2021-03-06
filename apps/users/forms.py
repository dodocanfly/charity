from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, \
    PasswordChangeForm
from django import forms
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': _('Imię'), 'autofocus': True})
        self.fields['last_name'].widget.attrs['placeholder'] = _('Nazwisko')
        self.fields['email'].widget.attrs.update({'placeholder': _('Email'), 'autofocus': False})
        self.fields['password1'].widget.attrs['placeholder'] = _('Hasło')
        self.fields['password2'].widget.attrs['placeholder'] = _('Powtórz hasło')

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = _('Email')
        self.fields['password'].widget.attrs['placeholder'] = _('Hasło')

    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        if not CustomUser.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(_('Użytkownik z podanym adresem email nie istnieje'))
        return self.cleaned_data['email']


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': _('Email'), 'readonly': True})
        self.fields['first_name'].widget.attrs['placeholder'] = _('Imię')
        self.fields['last_name'].widget.attrs['placeholder'] = _('Nazwisko')
        self.fields['city'].widget.attrs['placeholder'] = _('Miejscowość')

    def clean_email(self):
        if self.cleaned_data['email'] != CustomUser.objects.get(pk=self.instance.id).email:
            raise ValidationError(_('Adres e-mail zmienić może tylko administrator'))
        return self.cleaned_data['email']

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'city')


class SettingsForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = _('Aktualne hasło')
        self.fields['new_password1'].widget.attrs['placeholder'] = _('Nowe hasło')
        self.fields['new_password2'].widget.attrs['placeholder'] = _('Powtórz nowe hasło')
