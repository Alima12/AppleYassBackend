# Generated by Django 3.2.9 on 2022-01-14 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slideimages',
            options={'ordering': ['rank']},
        ),
        migrations.AddField(
            model_name='webtitles',
            name='our_address',
            field=models.TextField(null=True),
        ),
    ]
