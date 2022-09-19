# Generated by Django 3.2.12 on 2022-09-19 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_manunit_type_tables'),
    ]

    operations = [
        migrations.AddField(
            model_name='managementunit',
            name='lake_management_unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='common.lakemanagementunittype'),
        ),
        migrations.AlterField(
            model_name='managementunit',
            name='label',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='managementunittype',
            name='abbrev',
            field=models.CharField(db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='managementunittype',
            name='label',
            field=models.CharField(db_index=True, max_length=50),
        ),
    ]
