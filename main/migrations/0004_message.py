# Generated by Django 4.1.7 on 2023-03-03 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_thesis'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن پیام')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recieved_messages', to=settings.AUTH_USER_MODEL, verbose_name='گیرنده')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sended_messages', to=settings.AUTH_USER_MODEL, verbose_name='فرستنده')),
            ],
            options={
                'verbose_name': ('پیام',),
                'verbose_name_plural': 'پیام\u200cها',
            },
        ),
    ]
