# Generated by Django 4.1.7 on 2023-02-18 07:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_answer_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]