# Generated by Django 3.2.9 on 2021-11-26 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_review_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'managed': False},
        ),
    ]