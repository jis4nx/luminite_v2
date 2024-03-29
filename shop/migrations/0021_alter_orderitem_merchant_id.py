# Generated by Django 4.2.1 on 2023-11-29 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_user_type'),
        ('shop', '0020_productitem_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='merchant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sold_items', to='accounts.seller'),
        ),
    ]
