# Generated by Django 4.0.2 on 2022-03-04 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('networks_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('icon_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProductMerchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('awin_merchant_id', models.IntegerField(blank=True, null=True)),
                ('loader_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='networks_app.awinproductlink')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=1000)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('image_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('best_deal', models.BooleanField(default=False)),
                ('awin_deep_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('awin_product_id', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.productcategory')),
                ('loader_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='networks_app.awinproductlink')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.productmerchant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
