from rest_framework import serializers
from .models import *


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="customer-detail")

    class Meta:
        model = Customer
        fields = ['url', 'id', 'name', 'surname', 'email', 'phone']


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(max_length=45, write_only=True, style={
        'input_type': 'password'})
    customer = serializers.SlugRelatedField(
        queryset=Customer.objects.all(), slug_field='id', allow_null=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="account-detail")

    class Meta:
        model = Account
        fields = ['url', 'id', 'email', 'password', 'customer']


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-type-detail")

    class Meta:
        model = ProductType
        fields = ['url', 'id', 'name', 'size', 'servings',
                  'quantity', 'price']

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
    description = serializers.CharField(
        max_length=255, style={'type': 'textarea'})
    url = serializers.HyperlinkedIdentityField(
        view_name="product-flavour-detail")

    class Meta:
        model = ProductFlavour
        fields = ['url', 'id', 'name', 'description']


class ProductTopperSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-topper-detail")

    class Meta:
        model = ProductTopper
        fields = ['url', 'id', 'name', 'price']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Cena musi być większa niż 0.")
        return value


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.SlugRelatedField(
        queryset=ProductType.objects.all(), slug_field='name')
    flavour = serializers.SlugRelatedField(
        queryset=ProductFlavour.objects.all(), slug_field='name')
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail")

    class Meta:
        model = Product
        fields = ['url', 'id', 'name', 'price', 'type', 'flavour']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Cena musi być większa niż 0.")
        return value


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    customer = serializers.SlugRelatedField(
        queryset=Customer.objects.all(), slug_field='id')
    url = serializers.HyperlinkedIdentityField(
        view_name="order-detail")

    class Meta:
        model = Order
        fields = ['url', 'id', 'status', 'order_date',
                  'pickup_date', 'pickup_time', 'total', 'customer']

    def validate_pickup_date(self, value):
        if Order.clean() == False:
            raise serializers.ValidationError(
                "Data odbioru musi być późniejsza niż data zamówienia.")
        return value

    def validate_total(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Cena całkowita musi być większa niż 0.")
        return value

    # def validate(self, data):
    #     if self.data['order_date'] > self.data['pickup_date']:
    #         raise serializers.ValidationError(
    #             "Data odbioru musi być późniejsza niż data zamówienia.")


class OrderDetailsSerializer(serializers.HyperlinkedModelSerializer):
    special_request = serializers.CharField(max_length=255, allow_null=True)
    order = serializers.SlugRelatedField(
        queryset=Order.objects.all(), slug_field='id')
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field='name')
    topper = serializers.SlugRelatedField(
        queryset=ProductTopper.objects.all(), slug_field='name', allow_null=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="order-details-detail")

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
