# Generated by Django 4.2 on 2023-04-15 21:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
