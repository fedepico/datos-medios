from rest_framework import viewsets
from .models import Analisis, ResultadoCEP, ResultadoFDA
from .serializers import AnalisisSerializer, ResultadoCEPSerializer, ResultadoFDASerializer

class AnalisisViewSet(viewsets.ModelViewSet):
    queryset = Analisis.objects.all()
    serializer_class = AnalisisSerializer

class ResultadoCEPViewSet(viewsets.ModelViewSet):
    queryset = ResultadoCEP.objects.all()
    serializer_class = ResultadoCEPSerializer

class ResultadoFDAViewSet(viewsets.ModelViewSet):
    queryset = ResultadoFDA.objects.all()
    serializer_class = ResultadoFDASerializer
