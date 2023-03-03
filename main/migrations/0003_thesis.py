# Generated by Django 4.1.7 on 2023-03-03 06:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('refree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_thesises', to=settings.AUTH_USER_MODEL, verbose_name='داور')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_thesises', to=settings.AUTH_USER_MODEL, verbose_name='دانشجو')),
            ],
            options={
                'verbose_name': 'پایان\u200cنامه',
                'verbose_name_plural': 'پایان\u200cنامه\u200cها',
            },
        ),
    ]