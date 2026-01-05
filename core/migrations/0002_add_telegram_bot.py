# Generated manually for adding TelegramBot model

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_token', models.CharField(help_text='Telegram bot token from @BotFather', max_length=200, unique=True)),
                ('bot_name', models.CharField(blank=True, help_text='Bot display name (optional)', max_length=100, null=True)),
                ('admin_chat_ids', models.JSONField(default=list, help_text='List of Telegram user IDs allowed admin access (JSON array of integers)')),
                ('backup_interval_hours', models.PositiveIntegerField(default=24, help_text='Interval in hours for automatic database backups')),
                ('last_backup_at', models.DateTimeField(blank=True, help_text='Timestamp of the last successful backup', null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Whether the bot is active and responding to commands')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Telegram Bot',
                'verbose_name_plural': 'Telegram Bots',
                'ordering': ['-created_at'],
            },
        ),
    ]

