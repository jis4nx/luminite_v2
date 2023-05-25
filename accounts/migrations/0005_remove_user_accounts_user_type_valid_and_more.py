# Generated by Django 4.2.1 on 2023-05-25 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_type'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user',
            name='accounts_user_type_valid',
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(('type__in', ['C', 'S', 'O'])), name='accounts_user_type_valid'),
        ),
    ]