# Generated by Django 4.2.1 on 2023-05-12 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_productitem_product_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productitem',
            name='product_color',
            field=models.CharField(choices=[('RED', 'Red'), ('BLUE', 'Blue'), ('BLACK', 'Black'), ('GREEN', 'Green')], max_length=20),
        ),
    ]
