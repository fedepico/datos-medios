from django.contrib import admin
from .models import User
from .models import Account
from .models import Company

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Company)
