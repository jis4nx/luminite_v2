# Generated by Django 4.2.1 on 2023-06-23 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_alter_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='./image/default.jpg', upload_to='profile_pic'),
        ),
    ]
