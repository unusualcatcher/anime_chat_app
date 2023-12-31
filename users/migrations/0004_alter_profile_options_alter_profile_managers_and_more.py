# Generated by Django 4.2.3 on 2023-07-19 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_delete_user_profile_groups_profile_user_permissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={},
        ),
        migrations.AlterModelManagers(
            name='profile',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='password',
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
