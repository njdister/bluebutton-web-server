# Generated by Django 2.1.7 on 2019-05-28 16:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0037_auto_20171016_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserIdentificationLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('weight', models.IntegerField(default=0,
                 help_text='Integer value controlling the position of the label in lists.',
                 verbose_name='List Weight')),
                ('users', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
