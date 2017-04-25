# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-21 20:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_auto_20170421_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='comment',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='creation_DT',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='doctor_name',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='file_url',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='filename',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='left_eye_added_power',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='left_eye_axis',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='left_eye_base',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='left_eye_cylinder',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='left_eye_prism',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='left_eye_sphere',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='modification_DT',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='right_eye_added_power',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='right_eye_axis',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='right_eye_base',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='right_eye_cylinder',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='right_eye_prism',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='right_eye_sphere',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
