# Generated by Django 3.2.9 on 2021-12-03 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_color_orderitem_orders_productattributes_productimages_technicalattributes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='categtory',
            new_name='category',
        ),
    ]
