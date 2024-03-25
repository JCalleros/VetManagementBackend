# Generated by Django 4.1.13 on 2024-03-22 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0002_owner_phone_number_alter_owner_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='name',
        ),
        migrations.AddField(
            model_name='owner',
            name='full_name',
            field=models.CharField(db_index=True, default='DefaultName', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='owner',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='owner',
            name='contact',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pet',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pets.owner'),
        ),
    ]