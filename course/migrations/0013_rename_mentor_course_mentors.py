# Generated by Django 4.2 on 2023-04-14 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_rename_mentors_course_mentor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='mentor',
            new_name='mentors',
        ),
    ]
