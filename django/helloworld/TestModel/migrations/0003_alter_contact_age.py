# Generated by Django 3.2.8 on 2021-10-29 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0002_contact_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='age',
            field=models.IntegerField(default=0),
        ),
    ]