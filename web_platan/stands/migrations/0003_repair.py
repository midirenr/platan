# Generated by Django 4.1.3 on 2022-11-08 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stands', '0002_detailtype_devicetype_placeofproduction_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_serial_num', models.CharField(max_length=14)),
                ('message', models.CharField(max_length=255)),
                ('date_time', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'repair',
            },
        ),
    ]