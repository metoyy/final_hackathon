# Generated by Django 4.2 on 2023-04-11 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mentors', '0001_initial'),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('title', models.CharField(max_length=250, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('duration_months', models.IntegerField(default=3)),
                ('cover', models.ImageField(null=True, upload_to='images/')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='category.category')),
                ('languages', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='languages', to='category.language')),
                ('mentors', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='mentors', to='mentors.mentor')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='CourseImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150)),
                ('image', models.ImageField(upload_to='images/')),
                ('Course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='course.course')),
            ],
        ),
    ]