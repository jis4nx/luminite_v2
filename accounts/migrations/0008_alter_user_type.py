# Generated by Django 4.2.1 on 2023-06-23 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('CUSTOMER', 'Customer'), ('SELLER', 'Seller'), ('OTHER', 'Other')], default='OTHER', max_length=20),
        ),
    ]
