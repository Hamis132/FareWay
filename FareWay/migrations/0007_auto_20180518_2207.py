# Generated by Django 2.0.5 on 2018-05-18 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FareWay', '0006_auto_20180517_2249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attraction',
            old_name='coordinates',
            new_name='position',
        ),
    ]
