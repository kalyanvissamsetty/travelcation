# Generated by Django 3.2.2 on 2021-05-10 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
    ]
