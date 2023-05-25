# Generated by Django 4.2.1 on 2023-05-25 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_options_alter_user_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('CUSTOMER', 'Customer'), ('SELLER', 'Seller'), ('OTHER', 'Other')], default='OTHER', max_length=20),
        ),
    ]