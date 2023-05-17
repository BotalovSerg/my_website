# Generated by Django 4.2.1 on 2023-05-17 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_book_readers_alter_book_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbookrelation',
            name='rate',
            field=models.PositiveSmallIntegerField(choices=[(1, 'OK'), (2, 'Fine'), (3, 'Good'), (4, 'Amazig'), (5, 'Incredible')], null=True),
        ),
    ]
