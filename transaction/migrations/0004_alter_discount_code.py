# Generated by Django 3.2.9 on 2021-12-31 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_auto_20211221_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
