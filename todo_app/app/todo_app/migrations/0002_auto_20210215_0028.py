# Generated by Django 3.1.6 on 2021-02-15 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoapp',
            name='task_due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]