# Generated by Django 4.2 on 2023-04-14 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_rename_mentor_course_mentors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='languages',
        ),
    ]