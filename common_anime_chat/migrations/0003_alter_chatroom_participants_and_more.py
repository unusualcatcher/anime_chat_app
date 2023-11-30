# Generated by Django 4.2.3 on 2023-07-19 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_remove_user_groups_and_more'),
        ('common_anime_chat', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='participants',
            field=models.ManyToManyField(to='users.profile'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_receiver', to='users.profile'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_sender', to='users.profile'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]