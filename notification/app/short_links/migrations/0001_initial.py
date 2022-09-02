# Generated by Django 4.0 on 2022-09-02 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_link', models.CharField(blank=True, max_length=10, unique=True)),
                ('long_link', models.URLField()),
                ('active', models.BooleanField(default=True)),
                ('valid_to', models.DateTimeField(editable=False)),
                ('redirect_url', models.URLField()),
            ],
        ),
    ]
