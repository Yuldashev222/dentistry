# Generated by Django 4.1.7 on 2023-02-18 07:30

import django.contrib.auth.password_validation
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_answer_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, validators=[django.contrib.auth.password_validation.validate_password], verbose_name='password'),
        ),
    ]