# Generated by Django 4.0.2 on 2022-04-26 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_meeting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussioncommentvote',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.discussioncomment'),
        ),
        migrations.AlterField(
            model_name='discussionpostvote',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.discussionpost'),
        ),
        migrations.AlterField(
            model_name='discussionsubcommentvote',
            name='sub_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.discussionsubcomment'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.appointment', unique=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='token',
            field=models.CharField(max_length=100),
        ),
    ]