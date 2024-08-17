from django.db import models
from .user import User
from .company import Company
from django.utils import timezone

class Account(models.Model):
    """
    Entidad de la cuenta
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='account', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='employee_account', on_delete=models.CASCADE)
    last_change_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)