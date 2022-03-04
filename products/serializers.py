from rest_framework import serializers
from .models import (
    Product,
    ProductCategory,
    ProductMerchant,
)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'merchant',]


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductMerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMerchant
        fields = '__all__'