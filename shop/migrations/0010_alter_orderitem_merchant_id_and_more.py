# Generated by Django 4.2.1 on 2023-11-08 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_user_type'),
        ('shop', '0009_alter_orderitem_options_orderitem_merchant_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='merchant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchants', to='accounts.seller'),
        ),
        migrations.AlterField(
            model_name='productitem',
            name='product_color',
            field=models.CharField(blank=True, choices=[('RED', 'Red'), ('BLUE', 'Blue'), ('BLACK', 'Black'), ('GREEN', 'Green')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='productitem',
            name='product_size',
            field=models.CharField(blank=True, choices=[('S', 'S'), ('M', 'M'), ('X', 'X'), ('XL', 'XL'), ('XLL', 'XLL')], max_length=20, null=True),
        ),
    ]