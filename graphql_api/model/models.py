from django.db import models
# Create your models here.


class Commodity(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name+'\n'+self.description


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=80)
    address = models.CharField(max_length=250)

    class Meta:
        ordering = ('last_name',)

    def __str__(self):
        return self.first_name+' '+self.last_name


class Order(models.Model):
    client = models.ForeignKey(Client, related_name='orders', on_delete=models.CASCADE, null=True, blank=True)


class Basket(models.Model):
    commodity = models.ForeignKey(Commodity, related_name='basket', on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, related_name='basket', on_delete=models.CASCADE, null=True, blank=True)


class Pay(models.Model):
    order = models.ForeignKey(Order, related_name='pay', on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=14)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.price
