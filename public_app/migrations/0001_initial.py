# Generated by Django 3.2.4 on 2021-06-26 14:22

from django.db import migrations, models
import django.db.models.deletion
import django_pgschemas.schema
import django_pgschemas.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(max_length=63, unique=True, validators=[django_pgschemas.utils.check_schema_name])),
                ('name', models.CharField(max_length=100)),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(django_pgschemas.schema.SchemaDescriptor, models.Model),
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253)),
                ('folder', models.SlugField(blank=True, max_length=253)),
                ('is_primary', models.BooleanField(default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='public_app.client')),
            ],
            options={
                'abstract': False,
                'unique_together': {('domain', 'folder')},
            },
        ),
    ]
