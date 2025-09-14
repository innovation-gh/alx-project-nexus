from rest_framework import serializers
from .models import Product, Category  # Assumes your models are in place

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # All fields: name, description

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested category details
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'  # Includes name, description, price, category, created_at