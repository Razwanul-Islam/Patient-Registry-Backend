# Generated by Django 3.1.4 on 2021-08-07 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210805_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussioncomment',
            name='vote',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='discussionpost',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='discussionpost',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='discussionpost',
            name='patient_details',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='discussionpost',
            name='vote',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='discussionsubcomment',
            name='vote',
            field=models.IntegerField(null=True),
        ),
    ]
