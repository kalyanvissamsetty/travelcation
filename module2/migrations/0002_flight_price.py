# Generated by Django 3.2.2 on 2021-05-12 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]
