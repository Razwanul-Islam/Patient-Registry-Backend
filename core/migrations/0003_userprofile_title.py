# Generated by Django 3.1.4 on 2021-07-26 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_userprofile_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='title',
            field=models.CharField(default='Doctor', max_length=150),
        ),
    ]
