# Generated by Django 2.1 on 2019-02-25 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20190225_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='number_of_booking',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
