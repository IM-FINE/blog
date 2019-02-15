# Generated by Django 2.1.3 on 2018-12-16 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth', models.DateTimeField()),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('school', models.CharField(blank=True, max_length=100)),
                ('company', models.CharField(blank=True, max_length=100)),
                ('profession', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('aboutme', models.TextField(blank=True)),
                ('portrait', models.ImageField(blank=True, upload_to='images/portrait/p_%Y_%m_%d')),
                ('name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
