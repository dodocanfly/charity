from django.urls import path

from . import views

urlpatterns = [
    path('zarejestruj', views.RegisterView.as_view(), name='register'),
    path('aktywacja/<slug:uidb64>/<slug:token>', views.ActivateView.as_view(), name='activate'),
    path('profil', views.ProfileView.as_view(), name='profile'),
    path('ustawienia', views.SettingsView.as_view(), name='settings'),

    path('zaloguj', views.CustomLoginView.as_view(), name='login'),
    path('wyloguj', views.CustomLogoutView.as_view(), name='logout'),

    path('resetuj-haslo', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('resetuj-haslo/mail-wyslany', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('resetuj-haslo/<uidb64>/<token>', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('resetuj-haslo/gotowe', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
