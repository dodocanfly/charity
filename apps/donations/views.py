from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import DatabaseError
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.utils.translation import ugettext_lazy as _

from .forms import DonationForm
from .models import Donation, InstitutionType


class HomeView(View):
    def get(self, request):
        counters = {
            'bags': Donation.objects.aggregate(Sum('quantity')).get('quantity__sum'),
            'organizations': Donation.objects.aggregate(Count('institution', distinct=True)).get('institution__count'),
        }
        institutions_types = InstitutionType.objects.all()
        return render(request, 'donations/home.html', {
            'counters': counters,
            'institution_types': institutions_types,
        })


class FormView(LoginRequiredMixin, View):
    def get(self, request):
        form = DonationForm(request=request)
        return render(request, 'donations/form.html', {'form': form})

    def post(self, request):
        form = DonationForm(request.POST, request=request)
        if form.is_valid():
            donation = form.save()
            for cat in form.cleaned_data['categories']:
                donation.categories.add(cat)
            return redirect(reverse('form-confirm'))
        return render(request, 'donations/form.html', {'form': form})


class FormConfirmView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'donations/form-confirm.html')


class MyDonationsView(LoginRequiredMixin, View):
    def get(self, request):
        if request.GET.get('odbierz'):
            self.change_taken_status(request)
            return redirect(reverse('my-donations'))

        donations = Donation.objects.filter(user=request.user).order_by('-pick_up_date', 'institution__name')
        page = request.GET.get('page', 1)
        paginator = Paginator(donations, 5)
        try:
            donations = paginator.page(page)
        except PageNotAnInteger:
            donations = paginator.page(1)
        except EmptyPage:
            donations = paginator.page(paginator.num_pages)

        return render(request, 'donations/my-donations.html', {
            'donations': donations,
        })

    @staticmethod
    def donation_exists(request):
        return Donation.objects.filter(pk=request.GET.get('odbierz'), user=request.user, is_taken=False).exists()

    def change_taken_status(self, request):
        if self.donation_exists(request):
            try:
                Donation.objects.filter(pk=request.GET.get('odbierz')).update(is_taken=True)
            except DatabaseError:
                messages.error(request, _('Nie udało się zapisać zmian'))
            else:
                messages.success(request, _('Zmiany zapisane'))
        else:
            messages.error(request, _('Nie udało się znaleźć żądanej darowizny'))


def send_mail_view(request):
    subject = 'Wiadomość ze strony charity donations'
    name = request.GET.get('name', 'imię')
    surname = request.GET.get('surname', 'nazwisko')
    message = f'Wiadomość od <{name} {surname}>\n'
    message += request.GET.get('message', '')
    mail_from = 'info@dodocanfly.pl'
    mail_to = ['patryk@siatka.org']
    if message:
        try:
            send_mail(subject, message, mail_from, mail_to)
        except BadHeaderError:
            return HttpResponse(_('Nie udało się wysłać wiadomości'))
        return HttpResponse(_('Wiadomość wysłana'))
    else:
        return HttpResponse(_('Musisz podać treść wiadomości'))
