# Generated by Django 3.1.4 on 2021-02-07 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0008_auto_20200625_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, default='', help_text='Warning: if you change this email here, you must first use the button below to change the email in Users.', max_length=100),
        ),
    ]