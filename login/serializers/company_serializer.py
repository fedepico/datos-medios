from rest_framework import serializers
from login.models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'last_change_date', 'is_active']