from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.utils.translation import ugettext_lazy as _

from .forms import RegistrationForm, ProfileForm, CustomAuthForm, CustomPasswordResetForm, SettingsForm
from .models import CustomUser
from .tokens import account_activation_token


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = RegistrationForm
        return render(request, 'users/register_form.html', context={'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = _('Aktywuj swoje konto')
            message = render_to_string('users/activation_email.html', {
                'user': user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'users/register_done.html')
        return render(request, 'users/register_form.html', context={'form': form})


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'users/activation_done.html')
        else:
            return render(request, 'users/activation_invalid.html')


class CustomLoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthForm
    redirect_authenticated_user = True


class CustomLogoutView(auth_views.LogoutView):
    next_page = 'home'


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = CustomPasswordResetForm


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'users/profile_form.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Zmiany zostały pomyślnie zapisane.'))
            return redirect('profile')
        else:
            messages.error(request, _('Zmiany nie zostały zapisane - popraw poniższe błędy.'))
            return render(request, 'users/profile_form.html', {'form': form})


class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        form = SettingsForm(request.user)
        return render(request, 'users/settings_form.html', {'form': form})

    def post(self, request):
        form = SettingsForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Zmiany zostały pomyślnie zapisane.'))
            return redirect('settings')
        else:
            messages.error(request, _('Zmiany nie zostały zapisane - popraw poniższe błędy.'))
        return render(request, 'users/settings_form.html', {'form': form})
