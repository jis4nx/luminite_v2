# Generated by Django 4.2.1 on 2023-05-25 06:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_agun'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agun',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]