from rest_framework import serializers
from .models import *
from django.contrib.auth.models import *


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="customer-detail")
    orders = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='order-detail')

    class Meta:
        model = Customer
        fields = ['url', 'id', 'name', 'surname', 'email', 'phone', 'orders']


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email']


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-type-detail")
    products = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='product-detail')

    class Meta:
        model = ProductType
        fields = ['url', 'id', 'name', 'size', 'servings',
                  'quantity', 'price', 'products']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Ilość musi być większa niż 0.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Cena musi być większa niż 0.")
        return value


class ProductFlavourSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-flavour-detail")
    description = serializers.CharField(
        max_length=255, style={'type': 'textarea'})
    products = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='product-detail')

    class Meta:
        model = ProductFlavour
        fields = ['url', 'id', 'name', 'description', 'products']


class ProductTopperSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-topper-detail")
    products = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='product-detail')

    class Meta:
        model = ProductTopper
        fields = ['url', 'id', 'name', 'price', 'products']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Cena musi być większa niż 0.")
        return value


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail")
    type = serializers.SlugRelatedField(
        queryset=ProductType.objects.all(), slug_field='name')
    flavour = serializers.SlugRelatedField(
        queryset=ProductFlavour.objects.all(), slug_field='name')
    order_details = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='order-details-detail')

    class Meta:
        model = Product
        fields = ['url', 'id', 'name', 'type', 'flavour', 'order_details']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Cena musi być większa niż 0.")
        return value


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="order-detail")
    customer = serializers.SlugRelatedField(
        queryset=Customer.objects.all(), slug_field='id')
    order_details = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='order-details-detail')

    class Meta:
        model = Order
        fields = ['url', 'id', 'status', 'order_date',
                  'pickup_date', 'pickup_time', 'total', 'customer', 'order_details']

    def validate_total(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Cena całkowita musi być liczbą dodatnia.")
        return value

    def validate_pickup_date(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError(
                "Data odbioru musi być późniejsza niż data zamówienia.")
        return value


class OrderDetailsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="order-details-detail")
    special_request = serializers.CharField(
        max_length=255, style={'type': 'textarea'}, allow_null=True)
    order = serializers.SlugRelatedField(
        queryset=Order.objects.all(), slug_field='id')
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field='name')
    topper = serializers.SlugRelatedField(
        queryset=ProductTopper.objects.all(), slug_field='name', allow_null=True)

    class Meta:
        model = OrderDetails
        fields = ['url', 'id', 'quantity', 'price', 'special_request',
                  'order', 'product', 'topper']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Ilość musi być większa niż 0.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Cena musi być większa niż 0.")
        return value
