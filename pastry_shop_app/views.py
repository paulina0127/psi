from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import permissions
from django.contrib.auth.models import User
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter, FilterSet


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    name = 'customer-list'
    filterset_fields = ['surname', 'name']
    search_fields = ['id', 'surname', 'name']
    ordering_fields = ['id', 'surname']


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    name = 'customer-detail'


class AccountList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    name = 'account-list'
    search_fields = ['username']
    ordering_fields = ['id']


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    name = 'user-detail'


class ProductTypeFilter(FilterSet):
    min_quantity = NumberFilter(field_name='quantity', lookup_expr='gte')
    max_quantity = NumberFilter(field_name='quantity', lookup_expr='lte')
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = ProductType
        fields = ['name', 'min_quantity',
                  'max_quantity', 'min_price', 'max_price']


class ProductTypeList(generics.ListCreateAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    name = 'product-type-list'
    filterset_class = ProductTypeFilter
    search_fields = ['name']
    ordering_fields = ['id', 'price']


class ProductTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    name = 'product-type-detail'


class ProductFlavourList(generics.ListCreateAPIView):
    queryset = ProductFlavour.objects.all()
    serializer_class = ProductFlavourSerializer
    name = 'product-flavour-list'
    search_fields = ['name']
    ordering_fields = ['id']


class ProductFlavourDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductFlavour.objects.all()
    serializer_class = ProductFlavourSerializer
    name = 'product-flavour-detail'


class ProductTopperFilter(FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = ProductTopper
        fields = ['min_price', 'max_price']


class ProductTopperList(generics.ListCreateAPIView):
    queryset = ProductTopper.objects.all()
    serializer_class = ProductTopperSerializer
    name = 'product-topper-list'
    filterset_class = ProductTopperFilter
    search_fields = ['name']
    ordering_fields = ['id', 'price']


class ProductTopperDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductTopper.objects.all()
    serializer_class = ProductTopperSerializer
    name = 'product-topper-detail'


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    name = 'product-list'
    filterset_fields = ['type', 'flavour']
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'price']


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    name = 'product-detail'


class OrderFilter(FilterSet):
    from_order_date = DateTimeFilter(
        field_name='order_date', lookup_expr='gte')
    to_order_date = DateTimeFilter(field_name='order_date', lookup_expr='lte')
    from_pickup_date = DateTimeFilter(
        field_name='pickup_date', lookup_expr='gte')
    to_pickup_date = DateTimeFilter(
        field_name='pickup_date', lookup_expr='lte')
    min_total = NumberFilter(field_name='total', lookup_expr='gte')
    max_total = NumberFilter(field_name='total', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['status', 'customer', 'from_order_date',
                  'to_order_date', 'from_pickup_date', 'to_pickup_date', 'min_total', 'max_total']


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    name = 'order-list'
    filterset_class = OrderFilter
    search_fields = ['id']
    ordering_fields = ['id', 'order_date', 'pickup_date', 'total']


class OrderDetailsFilter(FilterSet):
    min_quantity = NumberFilter(field_name='quantity', lookup_expr='gte')
    max_quantity = NumberFilter(field_name='quantity', lookup_expr='lte')
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = OrderDetails
        fields = ['order', 'min_quantity',
                  'max_quantity', 'min_price', 'max_price']


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    name = 'order-detail'


class OrderDetailsList(generics.ListCreateAPIView):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer
    name = 'order-details-list'
    filterset_class = OrderDetailsFilter
    search_fields = ['order']
    ordering_fields = ['id']


class OrderDetailsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer
    name = 'order-details-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'customers': reverse(CustomerList.name, request=request),
                         'accounts': reverse(AccountList.name, request=request),
                         'product-types': reverse(ProductTypeList.name, request=request),
                         'product-flavours': reverse(ProductFlavourList.name, request=request),
                         'product-toppers': reverse(ProductTopperList.name, request=request),
                         'products': reverse(ProductList.name, request=request),
                         'orders': reverse(OrderList.name, request=request),
                         'order-details': reverse(OrderDetailsList.name, request=request)
                         })
