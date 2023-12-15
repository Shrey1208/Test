# serializers.py

from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem
from django.utils import timezone

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': []},  # Remove default unique validator to customize
        }

    def validate_name(self, value):
        instance = self.instance
        if instance and Customer.objects.filter(name=value).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("Customer with this name already exists.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, value):
        instance = self.instance
        if instance and Product.objects.filter(name=value).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("Product with this name already exists.")
        return value

    def validate_weight(self, value):
        if value <= 0 or value > 25:
            raise serializers.ValidationError("Weight must be a positive decimal not more than 25kg.")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def validate_order_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Order Date cannot be in the past.")
        return value

    def validate_items(self, value):
        total_weight = sum(item.product.weight * item.quantity for item in value)
        if total_weight > 150:
            raise serializers.ValidationError("Order cumulative weight must be under 150kg.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
