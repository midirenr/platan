# Generated by Django 4.1.3 on 2022-11-03 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stands', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('serial_number_modify', models.CharField(blank=True, max_length=5)),
            ],
            options={
                'verbose_name': 'Тип изделия',
                'verbose_name_plural': 'Тип изделия',
            },
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('serial_number_modify', models.CharField(blank=True, max_length=5)),
            ],
            options={
                'verbose_name': 'Тип устройства',
                'verbose_name_plural': 'Тип устройства',
            },
        ),
        migrations.CreateModel(
            name='PlaceOfProduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('serial_number_modify', models.CharField(blank=True, max_length=5)),
            ],
            options={
                'verbose_name': 'Место производства',
                'verbose_name_plural': 'Место производства',
            },
        ),
        migrations.AddField(
            model_name='serialnumboard',
            name='visual_inspection_author',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='serialnumboard',
            name='visual_inspection_datetime',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='statistic',
            name='manufacturer',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='devices',
            name='eth1addr_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mac2', to='stands.macs'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='eth2addr_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mac3', to='stands.macs'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='ethaddr_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mac1', to='stands.macs'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='serial_num_board_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.serialnumboard'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='serial_num_bp_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.serialnumbp'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='serial_num_case_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.serialnumcase'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='serial_num_package_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.serialnumpackage'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='serial_num_pcb_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.serialnumpcb'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='serial_num_pki_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.serialnumpki'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='serial_num_router_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.serialnumrouter'),
        ),
        migrations.AlterField(
            model_name='macs',
            name='device_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.devices'),
        ),
        migrations.AlterField(
            model_name='serialnumboard',
            name='device_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.devices'),
        ),
        migrations.AlterField(
            model_name='serialnumboard',
            name='visual_inspection',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='serialnumboard',
            name='visual_inspection_error_code',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='serialnumbp',
            name='device_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.devices'),
        ),
        migrations.AlterField(
            model_name='serialnumcase',
            name='device_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.devices'),
        ),
        migrations.AlterField(
            model_name='serialnumpackage',
            name='device_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.devices'),
        ),
        migrations.AlterField(
            model_name='serialnumpcb',
            name='device_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.devices'),
        ),
        migrations.AlterField(
            model_name='serialnumpki',
            name='device_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.devices'),
        ),
        migrations.AlterField(
            model_name='serialnumrouter',
            name='device_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stands.devices'),
        ),
        migrations.CreateModel(
            name='ModificationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('serial_number_modify', models.CharField(blank=True, max_length=5)),
                ('device_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stands.devicetype')),
            ],
            options={
                'verbose_name': 'Тип модификации',
                'verbose_name_plural': 'Тип модификации',
            },
        ),
        migrations.CreateModel(
            name='GenerateSerialNumbers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('detail_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stands.detailtype')),
                ('device_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stands.devicetype')),
                ('modification_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stands.modificationtype')),
                ('place_of_production', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stands.placeofproduction')),
            ],
        ),
    ]