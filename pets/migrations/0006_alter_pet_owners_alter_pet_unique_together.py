# Generated by Django 4.1.13 on 2024-03-24 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0005_alter_pet_unique_together_pet_owners_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='owners',
            field=models.ManyToManyField(blank=True, null=True, related_name='pets', to='pets.owner'),
        ),
        migrations.AlterUniqueTogether(
            name='pet',
            unique_together={('name', 'species', 'sex', 'breed', 'color')},
        ),
    ]