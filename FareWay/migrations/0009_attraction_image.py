# Generated by Django 2.0.3 on 2018-06-05 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FareWay', '0008_auto_20180519_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='attraction',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/imgs'),
        ),
    ]
