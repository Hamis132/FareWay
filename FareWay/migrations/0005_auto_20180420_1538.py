# Generated by Django 2.0.4 on 2018-04-20 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('FareWay', '0004_trip_usertrip'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripAttraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FareWay.Attraction')),
            ],
        ),
        migrations.RemoveField(
            model_name='usertrip',
            name='trip',
        ),
        migrations.RemoveField(
            model_name='usertrip',
            name='user',
        ),
        migrations.AddField(
            model_name='trip',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='trip',
            name='attractions',
        ),
        migrations.DeleteModel(
            name='UserTrip',
        ),
        migrations.AddField(
            model_name='tripattraction',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FareWay.Trip'),
        ),
        migrations.AddField(
            model_name='trip',
            name='attractions',
            field=models.ManyToManyField(through='FareWay.TripAttraction', to='FareWay.Attraction'),
        ),
    ]