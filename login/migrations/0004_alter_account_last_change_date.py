# Generated by Django 5.0.7 on 2024-07-21 17:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_alter_account_id_alter_company_id_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_change_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
