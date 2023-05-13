# Generated by Django 4.2.1 on 2023-05-12 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_productorder_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productitem',
            name='product_size',
            field=models.CharField(choices=[('S', 'S'), ('M', 'M'), ('X', 'X'), ('XL', 'XL'), ('XLL', 'XLL')], max_length=20),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='status',
            field=models.CharField(max_length=20),
        ),
    ]
