from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('przekaz-dary', views.FormView.as_view(), name='form'),
    path('przekaz-dary/potwierdzenie', views.FormConfirmView.as_view(), name='form-confirm'),
    path('moje-darowizny', views.MyDonationsView.as_view(), name='my-donations'),
    path('wyslij-wiadomosc', views.send_mail_view),
]
