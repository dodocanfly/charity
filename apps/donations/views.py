from django.db.models import Sum, Count
from django.shortcuts import render
from django.views import View

from .models import Donation, Institution


class HomeView(View):
    def get(self, request):
        counters = {
            'bags': Donation.objects.aggregate(Sum('quantity')).get('quantity__sum'),
            'organizations': Donation.objects.aggregate(Count('institution', distinct=True)).get('institution__count'),
        }
        institutions = {
            1: Institution.objects.filter(type=1),
            2: Institution.objects.filter(type=2),
            3: Institution.objects.filter(type=3),
        }
        return render(request, 'donations/home.html', {
            'counters': counters,
            'institutions': institutions,
        })


class FormView(View):
    def get(self, request):

        return render(request, 'donations/form.html')

    def post(self, request):
        import pprint
        form = pprint.pformat(request.POST)
        lista = request.POST.getlist('categories')
        return render(request, 'donations/form.html', {'form': form, 'lista': lista})
