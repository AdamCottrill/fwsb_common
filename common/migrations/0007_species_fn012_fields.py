# Generated by Django 2.2.27 on 2022-02-17 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20200622_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='species',
            name='flen2tlen_alpha',
            field=models.FloatField(blank=True, null=True, verbose_name='Intercept of FLEN-TLEN Regression'),
        ),
        migrations.AddField(
            model_name='species',
            name='flen2tlen_beta',
            field=models.FloatField(blank=True, null=True, verbose_name='Slope of FLEN-TLEN Regression'),
        ),
        migrations.AddField(
            model_name='species',
            name='flen_max',
            field=models.FloatField(blank=True, null=True, verbose_name='Maximim Fork Length (mm)'),
        ),
        migrations.AddField(
            model_name='species',
            name='flen_min',
            field=models.FloatField(blank=True, null=True, verbose_name='Minimum Fork Length (mm)'),
        ),
        migrations.AddField(
            model_name='species',
            name='k_max_error',
            field=models.FloatField(blank=True, null=True, verbose_name='Maximum K (FLEN) - error'),
        ),
        migrations.AddField(
            model_name='species',
            name='k_max_warn',
            field=models.FloatField(blank=True, null=True, verbose_name='Maximum K (FLEN) - warning'),
        ),
        migrations.AddField(
            model_name='species',
            name='k_min_error',
            field=models.FloatField(blank=True, null=True, verbose_name='Minimum K (TLEN) - error'),
        ),
        migrations.AddField(
            model_name='species',
            name='k_min_warn',
            field=models.FloatField(blank=True, null=True, verbose_name='Minimum K (TLEN) - warning'),
        ),
        migrations.AddField(
            model_name='species',
            name='rwt_max',
            field=models.FloatField(blank=True, null=True, verbose_name='Maximum Round Weight (g)'),
        ),
        migrations.AddField(
            model_name='species',
            name='rwt_min',
            field=models.FloatField(blank=True, null=True, verbose_name='Minimum Round Weight (g)'),
        ),
        migrations.AddField(
            model_name='species',
            name='tlen_max',
            field=models.FloatField(blank=True, null=True, verbose_name='Maximum Total Length (mm)'),
        ),
        migrations.AddField(
            model_name='species',
            name='tlen_min',
            field=models.FloatField(blank=True, null=True, verbose_name='Minimum Total Length (mm)'),
        ),
    ]
