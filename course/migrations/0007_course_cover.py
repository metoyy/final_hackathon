# Generated by Django 4.2 on 2023-04-13 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_remove_course_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='images/courses/cover/'),
        ),
    ]
