# Generated by Django 2.0.3 on 2018-06-22 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('FareWay', '0012_auto_20180607_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_name', models.CharField(max_length=30)),
                ('attractions', models.ManyToManyField(related_name='attractions', to='FareWay.Attraction')),
                ('end', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='end', to='FareWay.Attraction')),
                ('start', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='start', to='FareWay.Attraction')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='trip',
            name='attraction',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='end',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='start',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='user',
        ),
        migrations.DeleteModel(
            name='Trip',
        ),
    ]