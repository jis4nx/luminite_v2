# Generated by Django 4.2.1 on 2023-05-12 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_delete_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('CUSTOMER', 'Customer'), ('SELLER', 'Seller')], default='CUSTOMER', max_length=20),
        ),
    ]
