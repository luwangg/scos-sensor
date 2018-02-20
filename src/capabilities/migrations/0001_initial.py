# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-19 05:22
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Antenna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(help_text=b"Antenna make and model number. E.g. 'ARA CSB-16'.", max_length=255)),
                ('type', models.CharField(help_text=b"Antenna type. E.g. 'dipole'.", max_length=255, null=True)),
                ('low_frequency', models.FloatField(help_text=b'Low frequency of operational range. [Hz]', null=True)),
                ('high_frequency', models.FloatField(help_text=b'High frequency of operational range. [Hz]', null=True)),
                ('gain', models.FloatField(help_text=b'Antenna gain in direction of maximum radiation or reception. [dBi]', null=True)),
                ('horizontal_gain_pattern', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, help_text=b'Antenna gain pattern in horizontal plane. [dBi]', size=None)),
                ('vertical_gain_pattern', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, help_text=b'Antenna gain pattern in vertical plane. [dBi]', size=None)),
                ('horizontal_beam_width', models.FloatField(help_text=b'Horizontal 3-dB beamwidth. [degrees]', null=True)),
                ('vertical_beam_width', models.FloatField(help_text=b'Vertical 3-dB beamwidth. [degrees]', null=True)),
                ('cross_polar_discrimintation', models.FloatField(help_text=b'Cross-polarization discrimination.', null=True)),
                ('voltage_standing_wave_ratio', models.FloatField(help_text=b'Voltage standing wave ratio. [volts]', null=True)),
                ('cable_loss', models.FloatField(help_text=b'Loss for cable connecting antenna and preselector. [dB]', null=True)),
                ('steerable', models.NullBooleanField(help_text=b'Defines if the antenna is steerable or not.')),
                ('mobile', models.NullBooleanField(help_text=b'Defines if the antenna is mobile or not.')),
            ],
        ),
        migrations.CreateModel(
            name='DataExtractionUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(help_text=b"Make and model of DEU. E.g., 'Ettus B200'.", max_length=255)),
                ('low_frequency', models.FloatField(help_text=b'Low frequency of operational range. [Hz]', null=True)),
                ('high_frequency', models.FloatField(help_text=b'High frequency of operational range. [Hz]', null=True)),
                ('noise_figure', models.FloatField(help_text=b'Noise Figure. [dB]', null=True)),
                ('max_power', models.FloatField(help_text=b'Maximum input power. [dB]', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RFPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rf_path_number', models.PositiveSmallIntegerField(help_text=b'RF path number.', null=True)),
                ('low_frequency_passband', models.FloatField(help_text=b'Low frequency of filter 1-dB passband. [Hz]', null=True)),
                ('high_frequency_passband', models.FloatField(help_text=b'High frequency of filter 1-dB passband. [Hz]', null=True)),
                ('low_frequency_stopband', models.FloatField(help_text=b'Low frequency of filter 1-dB stopband. [Hz]', null=True)),
                ('high_frequency_stopband', models.FloatField(help_text=b'High frequency of filter 1-dB stopband. [Hz]', null=True)),
                ('lna_gain', models.FloatField(help_text=b'Gain of low noise amplifier. [dB]', null=True)),
                ('lna_noise_figure', models.FloatField(help_text=b'Noise figure of low noise amplifier. [dB]', null=True)),
                ('cal_source_type', models.CharField(help_text=b"E.g., 'calibrated noise source'.", max_length=255, null=True)),
                ('cal_source_enr', models.FloatField(help_text=b'Excess noise ratio of calibrated noise source at frequency of RF path. [dB]', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SignalConditioningUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='rfpath',
            name='signal_condition_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rf_path_spec', to='capabilities.SignalConditioningUnit'),
        ),
    ]