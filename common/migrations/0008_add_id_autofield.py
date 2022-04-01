# Generated by Django 3.2.12 on 2022-04-01 18:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_species_fn012_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grid5',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='lake',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='managementunit',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='species',
            name='flen2tlen_alpha',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-20.0), django.core.validators.MaxValueValidator(80.0)], verbose_name='Intercept of FLEN-TLEN Regression'),
        ),
        migrations.AlterField(
            model_name='species',
            name='flen2tlen_beta',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(1.25)], verbose_name='Slope of FLEN-TLEN Regression'),
        ),
        migrations.AlterField(
            model_name='species',
            name='flen_max',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2000)], verbose_name='Maximim Fork Length (mm)'),
        ),
        migrations.AlterField(
            model_name='species',
            name='flen_min',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(700)], verbose_name='Minimum Fork Length (mm)'),
        ),
        migrations.AlterField(
            model_name='species',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='species',
            name='k_max_error',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5.0)], verbose_name='Maximum K (FLEN) - error'),
        ),
        migrations.AlterField(
            model_name='species',
            name='k_max_warn',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4.0)], verbose_name='Maximum K (FLEN) - warning'),
        ),
        migrations.AlterField(
            model_name='species',
            name='k_min_error',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2.0)], verbose_name='Minimum K (TLEN) - error'),
        ),
        migrations.AlterField(
            model_name='species',
            name='k_min_warn',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1.5)], verbose_name='Minimum K (TLEN) - warning'),
        ),
        migrations.AlterField(
            model_name='species',
            name='rwt_max',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5000)], verbose_name='Maximum Round Weight (g)'),
        ),
        migrations.AlterField(
            model_name='species',
            name='rwt_min',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5000)], verbose_name='Minimum Round Weight (g)'),
        ),
        migrations.AlterField(
            model_name='species',
            name='tlen_max',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2000)], verbose_name='Maximum Total Length (mm)'),
        ),
        migrations.AlterField(
            model_name='species',
            name='tlen_min',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(700)], verbose_name='Minimum Total Length (mm)'),
        ),
    ]
