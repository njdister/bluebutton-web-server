# Generated by Django 2.1.2 on 2018-12-21 21:14

import apps.dot_ext.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dot_ext', '0012_auto_20181220_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='description',
            field=models.TextField(blank=True, default='', help_text='This is plain-text up to 1000 characters in length.', max_length=1000, validators=[apps.dot_ext.validators.validate_notags], verbose_name='Application Description'),
        ),
        migrations.AlterField(
            model_name='application',
            name='website_uri',
            field=models.URLField(blank=True, default='', help_text='This is typically a home/download website for the application. For example, https://www.example.org or http://www.example.org .', max_length=512, verbose_name='Website URI'),
        ),
    ]
