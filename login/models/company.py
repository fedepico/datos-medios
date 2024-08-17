from django.db import models
from django.utils import timezone

class Company(models.Model):
    """
    Entidad de la compañía
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField('Name', max_length = 100)
    last_change_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)