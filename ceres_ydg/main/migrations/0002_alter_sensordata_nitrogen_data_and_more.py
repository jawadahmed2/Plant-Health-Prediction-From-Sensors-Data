# Generated by Django 4.2.5 on 2023-10-06 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordata',
            name='nitrogen_data',
            field=models.SmallIntegerField(verbose_name='Nitrogen'),
        ),
        migrations.AlterField(
            model_name='sensordata',
            name='phosphorus_data',
            field=models.SmallIntegerField(verbose_name='Phosphorus'),
        ),
        migrations.AlterField(
            model_name='sensordata',
            name='potassium_data',
            field=models.SmallIntegerField(verbose_name='Potassium'),
        ),
    ]
