from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    UserSerializer, InstitutionSerializer, DonationSerializer,
    CategorySerializer, InstitutionTypeSerializer, InstitutionsInSerializer)
from apps.users.models import CustomUser
from apps.donations.models import Institution, Donation, Category, InstitutionType


class MyPageNumberPagination(PageNumberPagination):
    page_size = 5


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class InstitutionTypeViewSet(viewsets.ModelViewSet):
    queryset = InstitutionType.objects.all()
    serializer_class = InstitutionTypeSerializer
    # pagination_class = MyPageNumberPagination


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    # pagination_class = MyPageNumberPagination


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    # pagination_class = MyPageNumberPagination


class InstitutionsInViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionsInSerializer

    def get_queryset(self):
        categories = self.request.GET.get('categories')
        if categories is not None and len(categories):
            categories = categories.split(',')
            return Institution.objects.filter(categories__in=categories).distinct()
        return Institution.objects.all()
