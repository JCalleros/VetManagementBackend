# Generated by Django 4.1.13 on 2024-03-22 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0003_remove_owner_name_owner_full_name_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pet',
            unique_together={('name', 'species', 'sex', 'owner')},
        ),
    ]
