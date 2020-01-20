from rest_framework import serializers

from apps.donations.models import Institution, Category, InstitutionType, Donation
from apps.users.models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'url', 'username', 'email', 'groups']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class InstitutionTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InstitutionType
        fields = ['id', 'name', 'description']


class InstitutionSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Institution
        fields = ['name', 'description', 'type', 'categories']


class DonationSerializer(serializers.ModelSerializer):
    institution = InstitutionSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'quantity', 'institution', 'categories']


class InstitutionsInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name', 'description']
