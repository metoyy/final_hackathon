# Generated by Django 4.2 on 2023-04-19 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_telegram_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='tg_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
