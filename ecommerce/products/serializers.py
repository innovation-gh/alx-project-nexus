from rest_framework import serializers
from .models import Product, Category, CartItem, Order
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=True,
        required=False
    )

    class Meta:
        model = Product
        fields = '__all__'

    def validate_image(self, value):
        if value:
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError("Image size should not exceed 2MB.")
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError("File must be an image.")
        return value

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        product = Product.objects.create(**validated_data)
        if image:
            product.image = image
            product.save()
        return product

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.category = validated_data.get('category', instance.category)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        if image is not None:
            instance.image = image
        instance.save()
        return instance

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True,
        required=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'product_id', 'quantity', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return CartItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    items = CartItemSerializer(many=True, read_only=True)  # Read-only for GET
    item_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=CartItem.objects.all(), write_only=True),
        write_only=True,
        required=False
    )

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 'created_at', 'items', 'item_ids']

    def create(self, validated_data):
        item_ids = validated_data.pop('item_ids', [])
        user = self.context['request'].user
        order = Order.objects.create(user=user, total_amount=0, status='pending')
        
        # Calculate total and link items
        total = 0
        for item_id in item_ids:
            cart_item = CartItem.objects.get(id=item_id, user=user)
            total += cart_item.product.price * cart_item.quantity
            cart_item.delete()  # Optional: Clear cart items after order
        order.total_amount = total
        order.save()
        return order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', '')
        )
        return user