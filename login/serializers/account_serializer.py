from login.models import Account, Company
from rest_framework import serializers
from .company_serializer import CompanySerializer

class AccountSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Account
        fields = ['id', 'company', 'last_change_date', 'is_active']