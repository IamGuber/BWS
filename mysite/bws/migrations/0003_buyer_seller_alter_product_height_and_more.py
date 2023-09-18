# Generated by Django 4.2.5 on 2023-09-15 16:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bws', '0002_product_height_product_length_product_thickness_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('tel_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Lithuanian phone number must start with +370 and have 8 additional digits.', regex='^\\+370\\d{8}$')], verbose_name='Telephone Number')),
                ('info', models.TextField(max_length=5000, verbose_name='Additional Information')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('tel_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Lithuanian phone number must start with +370 and have 8 additional digits.', regex='^\\+370\\d{8}$')], verbose_name='Telephone Number')),
                ('info', models.TextField(max_length=5000, verbose_name='Additional Information')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='height',
            field=models.IntegerField(default=0, verbose_name='Height(mm)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='length',
            field=models.IntegerField(default=0, verbose_name='Length(mm)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='thickness',
            field=models.IntegerField(default=0, verbose_name='Thickness(mm)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='width',
            field=models.IntegerField(default=0, verbose_name='Width(mm)'),
        ),
    ]
