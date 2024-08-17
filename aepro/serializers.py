from rest_framework import serializers
from .models import Analisis, ResultadoCEP, ResultadoFDA

class AnalisisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analisis
        fields = '__all__'

class ResultadoCEPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoCEP
        fields = '__all__'

class ResultadoFDASerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoFDA
        fields = '__all__'
