from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import AnalisisViewSet, ResultadoCEPViewSet, ResultadoFDAViewSet

router = DefaultRouter()
router.register(r'analisis', AnalisisViewSet)
router.register(r'resultadocep', ResultadoCEPViewSet)
router.register(r'resultadofda', ResultadoFDAViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
