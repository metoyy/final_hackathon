# Generated by Django 4.2 on 2023-04-14 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_course_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='mentors',
            new_name='mentor',
        ),
    ]
