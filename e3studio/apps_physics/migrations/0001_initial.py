# Generated by Django 2.2.10 on 2020-11-23 08:40

import apps_physics.ultilities
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppsPhysics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appname', models.CharField(max_length=200, null=True)),
                ('front_image', models.ImageField(blank=True, null=True, upload_to=apps_physics.ultilities.apps_physics_image_path_front, verbose_name='front image')),
                ('top_image', models.ImageField(blank=True, null=True, upload_to=apps_physics.ultilities.apps_physics_image_path_top, verbose_name='top image')),
                ('right_image', models.ImageField(blank=True, null=True, upload_to=apps_physics.ultilities.apps_physics_image_path_right, verbose_name='right image')),
                ('right_image_web', models.CharField(max_length=200, null=True)),
                ('icon', models.CharField(max_length=200, null=True)),
                ('web', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(max_length=300, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]