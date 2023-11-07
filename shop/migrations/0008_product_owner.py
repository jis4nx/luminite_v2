# Generated by Django 4.2.1 on 2023-11-02 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_user_type'),
        ('shop', '0007_productitem_attributes'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='accounts.seller'),
        ),
    ]