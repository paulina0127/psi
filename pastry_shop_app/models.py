from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
import datetime


class Customer(models.Model):
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField()

    def __str__(self) -> str:
        return self.name + " " + self.surname


class Account(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=45)
    customer = models.ForeignKey(
        Customer, related_name='accounts', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.email


class ProductType(models.Model):
    name = models.CharField(max_length=45)
    size = models.CharField(max_length=45)
    servings = models.CharField(max_length=45)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self) -> str:
        return self.size + " " + self.name


class ProductFlavour(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class ProductTopper(models.Model):
    name = models.CharField(max_length=45)
    price = models.FloatField()

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=45, blank=True)
    price = models.FloatField(blank=True)
    type = models.ForeignKey(
        ProductType, related_name='products', on_delete=models.CASCADE)
    flavour = models.ForeignKey(
        ProductFlavour, related_name='products', on_delete=models.CASCADE)
    topper = models.ForeignKey(
        ProductTopper, related_name='products', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.flavour.name + " " + self.type.size + " " + self.type.name

        if self.topper:
            self.price = self.type.price + self.topper.price
        else:
            self.price = self.type.price
        super(Product, self).save(*args, **kwargs)


class CustomProduct(models.Model):
    name = models.CharField(max_length=45, blank=True)
    price = models.FloatField(blank=True)
    special_request = models.CharField(max_length=255, blank=True, null=True)
    type = models.ForeignKey(
        ProductType, related_name='custom_products', on_delete=models.CASCADE)
    flavour = models.ForeignKey(
        ProductFlavour, related_name='custom_products', on_delete=models.CASCADE)
    topper = models.ForeignKey(
        ProductTopper, related_name='custom_products', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.flavour.name + " " + self.type.size + " " + self.type.name

        if self.topper:
            self.price = self.type.price + self.topper.price
        else:
            self.price = self.type.price
        super(CustomProduct, self).save(*args, **kwargs)


class Order(models.Model):
    NEW = "New"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    status_choices = ((NEW, "New"), (IN_PROGRESS,
                      "In progress"), (COMPLETED, "Completed"), (CANCELLED, "Cancelled"))

    status = models.CharField(max_length=45, choices=status_choices,
                              blank=True)
    order_date = models.DateField(default=datetime.date.today, blank=True)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    total = models.FloatField()
    customer = models.ForeignKey(
        Customer, related_name='orders', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Nr: " + str(self.id)

    def save(self, *args, **kwargs):
        self.status = "New"
        super(Order, self).save(*args, **kwargs)


class OrderDetails(models.Model):
    quantity = models.IntegerField()
    order = models.ForeignKey(
        Order, related_name='order_details', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_details', on_delete=models.CASCADE, blank=True, null=True)
    custom_product = models.ForeignKey(
        CustomProduct, related_name='order_details', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        if self.product:
            return self.product.name + ": " + str(self.quantity)
        elif self.custom_product:
            return self.custom_product.name + ": " + str(self.quantity)

    def clean(self):
        if self.product and self.custom_product:
            raise ValidationError(
                "Tylko jeden rodzaj produktu może być wybrany.")
        elif self.product is None and self.custom_product is None:
            "Jeden z produktów musi zostać wybrany."
