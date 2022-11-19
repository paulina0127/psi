from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
    # customers
    path('customers', views.CustomerList.as_view(),
         name=views.CustomerList.name),
    path('customers/<int:pk>', views.CustomerDetail.as_view(),
         name=views.CustomerDetail.name),
    # accounts
    path('accounts', views.AccountList.as_view(),
         name=views.AccountList.name),
    path('accounts/<int:pk>', views.AccountDetail.as_view(),
         name=views.AccountDetail.name),
    # product types
    path('product-types', views.ProductTypeList.as_view(),
         name=views.ProductTypeList.name),
    path('product-types/<int:pk>', views.ProductTypeDetail.as_view(),
         name='product-type-detail'),
    # product flavours
    path('product-flavours', views.ProductFlavourList.as_view(),
         name=views.ProductFlavourList.name),
    path('product-flavours/<int:pk>', views.ProductFlavourDetail.as_view(),
         name=views.ProductFlavourDetail.name),
    # product toppers
    path('product-toppers', views.ProductTopperList.as_view(),
         name=views.ProductTopperList.name),
    path('product-toppers/<int:pk>', views.ProductTopperDetail.as_view(),
         name=views.ProductTopperDetail.name),
    # products
    path('products', views.ProductList.as_view(),
         name=views.ProductList.name),
    path('products/<int:pk>', views.ProductDetail.as_view(),
         name=views.ProductDetail.name),
    # custom products
    path('custom-products', views.CustomProductList.as_view(),
         name=views.CustomProductList.name),
    path('custom-products/<int:pk>', views.CustomProductDetail.as_view(),
         name=views.CustomProductDetail.name),
    # order
    path('orders', views.OrderList.as_view(),
         name=views.OrderList.name),
    path('orders/<int:pk>', views.OrderDetail.as_view(),
         name=views.OrderDetail.name),
    # order details
    path('order-details', views.OrderDetailsList.as_view(),
         name=views.OrderDetailsList.name),
    path('order-details/<int:pk>', views.OrderDetailsDetail.as_view(),
         name=views.OrderDetailsDetail.name)
]
