# Generated by Django 3.1.4 on 2021-09-27 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210813_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussionpost',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.discussioncategory'),
        ),
    ]
