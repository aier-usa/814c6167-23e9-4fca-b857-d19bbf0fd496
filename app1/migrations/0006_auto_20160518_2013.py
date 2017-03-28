# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 01:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0005_password_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('purpose', models.CharField(max_length=255, null=True)),
                ('creationDT', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordAccessPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationshipDT', models.DateTimeField(null=True)),
                ('access_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.AccessPoint')),
            ],
        ),
        migrations.AddField(
            model_name='password',
            name='user',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='ownership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='passwordaccesspoint',
            name='password',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Password'),
        ),
        migrations.AddField(
            model_name='password',
            name='access_points',
            field=models.ManyToManyField(through='app1.PasswordAccessPoint', to='app1.AccessPoint'),
        ),
    ]