# Generated by Django 3.1.4 on 2021-07-31 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210731_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldofrecord',
            name='hint',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fieldofrecord',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='fieldofrecord',
            name='type',
            field=models.TextField(),
        ),
    ]
