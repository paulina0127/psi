from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(ProductType)
admin.site.register(ProductFlavour)
admin.site.register(ProductTopper)
admin.site.register(Product)
admin.site.register(CustomProduct)
admin.site.register(Order)
admin.site.register(OrderDetails)
