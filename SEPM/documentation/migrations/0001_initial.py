# Generated by Django 5.1.6 on 2025-03-05 14:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipment', '0001_initial'),
        ('parts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('document_type', models.CharField(choices=[('drawing', 'Drawing'), ('manual', 'Manual'), ('bom', 'Bill of Materials'), ('datasheet', 'Datasheet'), ('certificate', 'Certificate'), ('report', 'Report'), ('other', 'Other')], max_length=20)),
                ('file', models.FileField(upload_to='documents/')),
                ('filename', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('revision', models.CharField(blank=True, max_length=20)),
                ('is_current', models.BooleanField(default=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('equipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.equipment')),
                ('part', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='parts.part')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExportLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('export_type', models.CharField(choices=[('equipment', 'Equipment Export'), ('parts', 'Parts Export'), ('bom', 'BOM Export')], max_length=20)),
                ('file', models.FileField(upload_to='exports/')),
                ('items_exported', models.IntegerField(default=0)),
                ('exported_at', models.DateTimeField(auto_now_add=True)),
                ('exported_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImportLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_type', models.CharField(choices=[('equipment', 'Equipment Import'), ('parts', 'Parts Import'), ('bom', 'BOM Import'), ('stock', 'Stock Update')], max_length=20)),
                ('file', models.FileField(upload_to='imports/')),
                ('status', models.CharField(default='processing', max_length=20)),
                ('items_processed', models.IntegerField(default=0)),
                ('items_created', models.IntegerField(default=0)),
                ('items_updated', models.IntegerField(default=0)),
                ('items_failed', models.IntegerField(default=0)),
                ('log_details', models.TextField(blank=True)),
                ('imported_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('imported_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
