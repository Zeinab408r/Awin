# Generated by Django 4.0.2 on 2022-03-04 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AwinProductLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('link_address', models.CharField(max_length=2000)),
                ('state', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('ON_HOLD', 'ON_HOLD'), ('DELETED', 'DELETED')], max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
