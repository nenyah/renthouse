# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 04:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0003_auto_20161124_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='houseinfo',
            name='housetype',
            field=models.CharField(blank=True, choices=[('四室两厅两卫', '四室两厅两卫'), ('一室一厅一卫', '一室一厅一卫'), ('二室一厅一卫', '二室一厅一卫'), ('三室一厅一卫', '三室一厅一卫'), ('三室两厅两卫', '三室两厅两卫'), ('三室一厅两卫', '三室一厅两卫')], max_length=200),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='sex',
            field=models.CharField(choices=[('男', '男'), ('保密', '保密'), ('女', '女')], default='保密', max_length=10),
        ),
    ]
