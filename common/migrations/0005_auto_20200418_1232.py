# Generated by Django 2.2.12 on 2020-04-18 16:32

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("common", "0004_auto_20200417_1055")]

    operations = [
        migrations.AddField(
            model_name="lake",
            name="centroid_ontario",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True, null=True, srid=4326
            ),
        ),
        migrations.AddField(
            model_name="lake",
            name="envelope_ontario",
            field=django.contrib.gis.db.models.fields.PolygonField(
                blank=True, null=True, srid=4326
            ),
        ),
    ]
