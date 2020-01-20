from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

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
