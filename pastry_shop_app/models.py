from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    email = models.EmailField()
    phone = PhoneNumberField()
    owner = models.OneToOneField(
        'auth.User', related_name='accounts', on_delete=models.CASCADE, blank=True, null=True)
    # owner = models.ForeignKey(
    #     'auth.User', related_name='accounts', on_delete=models.CASCADE, unique=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.name + " " + self.surname


class ProductType(models.Model):
    name = models.CharField(max_length=45)
    size = models.CharField(max_length=45)
    servings = models.CharField(max_length=45)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.size + " " + self.name
        super(ProductType, self).save(*args, **kwargs)


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
    type = models.ForeignKey(
        ProductType, related_name='products', on_delete=models.CASCADE)
    flavour = models.ForeignKey(
        ProductFlavour, related_name='products', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.flavour.name + " " + self.type.name
        super(Product, self).save(*args, **kwargs)


class Order(models.Model):
    NEW = "New"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    STATUS_CHOICES = ((NEW, "New"), (IN_PROGRESS,
                      "In progress"), (COMPLETED, "Completed"), (CANCELLED, "Cancelled"))

    status = models.CharField(max_length=45, choices=STATUS_CHOICES,
                              blank=True)
    order_date = models.DateField(auto_now_add=True, blank=True)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    total = models.FloatField(default=0, blank=True)
    customer = models.ForeignKey(
        Customer, related_name='orders', on_delete=models.CASCADE)
    owner = models.ForeignKey(
        'auth.User', related_name='orders', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return "Nr: " + str(self.id)

    def save(self, *args, **kwargs):
        if not self.status:
            self.status = "New"
        super(Order, self).save(*args, **kwargs)


class OrderDetails(models.Model):
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    special_request = models.CharField(max_length=255, blank=True, null=True)
    order = models.ForeignKey(
        Order, related_name='order_details', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_details', on_delete=models.CASCADE)
    topper = models.ForeignKey(
        ProductTopper, related_name='order_details', on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(
        'auth.User', related_name='order_details', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.product.name + ": " + str(self.quantity)

    def save(self, *args, **kwargs):
        if self.topper:
            self.price = (self.quantity * self.product.type.price) + \
                (self.quantity * self.topper.price)
        else:
            self.price = self.quantity * self.product.type.price

        self.order.total += self.price
        self.order.save(update_fields=['total'])
        super(OrderDetails, self).save(*args, **kwargs)
