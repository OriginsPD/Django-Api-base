# Generated by Django 4.1.4 on 2022-12-09 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_remove_profile_alias_remove_user_profile_pic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default=1, upload_to='img_path'),
            preserve_default=False,
        ),
    ]
