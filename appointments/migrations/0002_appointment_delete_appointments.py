# Generated by Django 4.1.13 on 2024-03-12 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0001_initial'),
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('time', models.TimeField()),
                ('details', models.TextField(blank=True, null=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pet')),
            ],
        ),
        migrations.DeleteModel(
            name='Appointments',
        ),
    ]
