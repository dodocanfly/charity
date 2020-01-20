from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('form', views.FormView.as_view(), name='form'),
    path('form-confirm', views.FormConfirmView.as_view(), name='form-confirm'),
]
