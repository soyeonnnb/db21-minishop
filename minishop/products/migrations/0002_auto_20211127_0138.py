# Generated by Django 3.2.9 on 2021-11-26 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'managed': False, 'verbose_name_plural': 'Product Categories'},
        ),
    ]
