# Generated by Django 3.1.6 on 2021-02-15 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAPIKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(blank=True, default='', max_length=2000)),
                ('user_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user_id'],
            },
        ),
        migrations.CreateModel(
            name='ToDoApp',
            fields=[
                ('taskid', models.AutoField(primary_key=True, serialize=False)),
                ('task_title', models.CharField(blank=True, default='', max_length=2000)),
                ('task_description', models.TextField(blank=True, default='')),
                ('task_state', models.CharField(blank=True, choices=[('1', 'Todo'), ('2', 'In Progress'), ('3', 'Done')], default='1', max_length=2, null=True)),
                ('task_due_date', models.DateField()),
                ('user_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['taskid'],
            },
        ),
    ]