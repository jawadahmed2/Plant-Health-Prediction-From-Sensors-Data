# Generated by Django 4.2.5 on 2023-10-08 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_rename_test2_test'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AlterField(
            model_name='sensordata',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]