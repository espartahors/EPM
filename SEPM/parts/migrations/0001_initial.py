# Generated by Django 5.1.6 on 2025-03-05 14:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PartCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Part Categories',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('contact_person', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('address', models.TextField(blank=True)),
                ('website', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_number', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('unit', models.CharField(default='pcs', max_length=20)),
                ('current_stock', models.PositiveIntegerField(default=0)),
                ('min_stock_level', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('active', 'Active'), ('obsolete', 'Obsolete'), ('discontinued', 'Discontinued')], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parts.partcategory')),
            ],
        ),
        migrations.CreateModel(
            name='PartSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_part_number', models.CharField(blank=True, max_length=50)),
                ('unit_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('lead_time_days', models.PositiveIntegerField(blank=True, null=True)),
                ('is_preferred', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parts.part')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parts.supplier')),
            ],
            options={
                'unique_together': {('part', 'supplier')},
            },
        ),
        migrations.AddField(
            model_name='part',
            name='suppliers',
            field=models.ManyToManyField(blank=True, through='parts.PartSupplier', to='parts.supplier'),
        ),
    ]
