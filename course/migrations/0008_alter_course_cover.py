# Generated by Django 4.2 on 2023-04-13 19:56

import course.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_course_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
