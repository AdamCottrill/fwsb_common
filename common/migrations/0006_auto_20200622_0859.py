# Generated by Django 2.2.13 on 2020-06-22 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20200418_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grid5',
            name='grid',
            field=models.CharField(db_index=True, max_length=4),
        ),
    ]