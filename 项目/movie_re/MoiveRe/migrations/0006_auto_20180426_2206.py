# Generated by Django 2.0.2 on 2018-04-26 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MoiveRe', '0005_movieratingavg_movieratingtimes'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('user', 'movie')},
        ),
    ]
