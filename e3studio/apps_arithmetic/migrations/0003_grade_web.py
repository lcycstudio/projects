# Generated by Django 2.2.10 on 2020-10-20 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_arithmetic', '0002_auto_20201019_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='web',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
