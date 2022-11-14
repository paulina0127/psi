from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)

    class Meta:
        ordering = ('surname',)


class Account(models.Model):
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    customer = models.ForeignKey(
        Customer, related_name='accounts', on_delete=models.CASCADE, null=True)


class ProductType(models.Model):
    name = models.CharField(max_length=45)
    size = models.CharField(max_length=45)
    servings = models.CharField(max_length=45)
    quantity = models.IntegerField()
    price = models.FloatField()


class ProductFlavour(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)


class ProductTopper(models.Model):
    name = models.CharField(max_length=45)
    price = models.FloatField()


class Product(models.Model):
    name = models.CharField(max_length=45)
    price = models.FloatField()
    type = models.ForeignKey(
        ProductType, related_name='products', on_delete=models.CASCADE)
    flavour = models.ForeignKey(
        ProductFlavour, related_name='products', on_delete=models.CASCADE)
    topper = models.ForeignKey(
        ProductTopper, related_name='products', on_delete=models.CASCADE, blank=True, null=True)


class CustomProduct(models.Model):
    name = models.CharField(max_length=45)
    price = models.FloatField()
    special_request = models.CharField(max_length=255, blank=True, null=True)
    type = models.ForeignKey(
        ProductType, related_name='custom_products', on_delete=models.CASCADE)
    flavour = models.ForeignKey(
        ProductFlavour, related_name='custom_products', on_delete=models.CASCADE)
    topper = models.ForeignKey(
        ProductTopper, related_name='custom_products', on_delete=models.CASCADE, blank=True, null=True)


class Order(models.Model):
    status = models.CharField(max_length=45)
    order_date = models.DateField()
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    total = models.FloatField()
    customer = models.ForeignKey(
        Customer, related_name='orders', on_delete=models.CASCADE)


class OrderDetails(models.Model):
    quantity = models.IntegerField()
    order = models.ForeignKey(
        Order, related_name='order_details', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_details', on_delete=models.CASCADE, null=True)
    custom_product = models.ForeignKey(
        CustomProduct, related_name='order_details', on_delete=models.CASCADE, null=True)
