# Generated by Django 3.1.4 on 2021-10-16 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_delete_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='draft', max_length=80)),
                ('payment_method', models.CharField(max_length=150, null=True)),
                ('transaction_id', models.CharField(max_length=150, null=True)),
                ('payment_number', models.IntegerField(null=True)),
                ('appointment_time', models.DateField(null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctorProfile', to='core.userprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patientProfile', to='core.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
