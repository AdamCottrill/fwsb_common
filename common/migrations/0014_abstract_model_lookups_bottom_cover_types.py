# Generated by Django 3.2.12 on 2022-10-03 14:30

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_add_contstraints_to_management_unit_type_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='BottomType',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('obsolete_date', models.DateTimeField(blank=True, null=True)),
                ('abbrev', models.CharField(db_index=True, max_length=2, unique=True)),
                ('label', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
            options={
                'ordering': ['abbrev'],
                'abstract': False,
            },
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CoverType',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('obsolete_date', models.DateTimeField(blank=True, null=True)),
                ('abbrev', models.CharField(db_index=True, max_length=2, unique=True)),
                ('label', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
            options={
                'ordering': ['abbrev'],
                'abstract': False,
            },
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
