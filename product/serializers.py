from rest_framework import serializers
from product.models import Product, ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'title', 'slug', 'sub_categories']


class ProductSerializer(serializers.ModelSerializer):
    product_per_category = ProductCategorySerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
