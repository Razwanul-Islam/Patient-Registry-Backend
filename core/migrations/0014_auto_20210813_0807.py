# Generated by Django 3.1.4 on 2021-08-13 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20210812_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussioncommentvote',
            name='down_vote',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='discussioncommentvote',
            name='up_vote',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='discussionpostvote',
            name='down_vote',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='discussionpostvote',
            name='up_vote',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='discussionsubcommentvote',
            name='down_vote',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='discussionsubcommentvote',
            name='up_vote',
            field=models.BooleanField(default=False),
        ),
    ]
