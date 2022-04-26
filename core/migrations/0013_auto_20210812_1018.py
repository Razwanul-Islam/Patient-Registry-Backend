# Generated by Django 3.1.4 on 2021-08-12 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210812_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussioncommentvote',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.userprofile'),
        ),
        migrations.AlterField(
            model_name='discussionpostvote',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.userprofile'),
        ),
        migrations.AlterField(
            model_name='discussionsubcommentvote',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.userprofile'),
        ),
    ]
