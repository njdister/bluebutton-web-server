# Generated by Django 2.2.22 on 2021-05-13 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('mymedicare_cb', '0001_initial'), ('mymedicare_cb', '0002_remove_anonuserstate_session_key')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnonUserState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(db_index=True, default='', max_length=64)),
                ('next_uri', models.CharField(default='', max_length=512)),
            ],
        ),
    ]
