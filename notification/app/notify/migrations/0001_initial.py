# Generated by Django 4.0 on 2022-08-29 18:29

import uuid

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notify', 'create_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationLog',
            fields=[
                ('notification_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('guid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('locked', models.BooleanField(blank=True, default=False, null=True)),
                ('stage', models.CharField(blank=True, choices=[('new', 'new'), ('failed', 'failed'), ('success', 'success')], default='new', max_length=20, null=True, verbose_name='type')),
                ('type', models.CharField(blank=True, choices=[('like', 'like'), ('mass_mail', 'mass_mail')], default='', max_length=20, null=True, verbose_name='type')),
            ],
        ),
    ]