# Generated by Django 4.1.13 on 2024-03-24 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0004_alter_pet_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pet',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='pet',
            name='owners',
            field=models.ManyToManyField(blank=True, related_name='pets', to='pets.owner'),
        ),
        migrations.RemoveField(
            model_name='pet',
            name='owner',
        ),
    ]