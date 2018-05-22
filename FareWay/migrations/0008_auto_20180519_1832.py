# Generated by Django 2.0.5 on 2018-05-19 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FareWay', '0007_auto_20180518_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attraction',
            name='position',
        ),
        migrations.AddField(
            model_name='attraction',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='attraction',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]