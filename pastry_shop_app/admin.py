from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(ProductType)
admin.site.register(ProductFlavour)
admin.site.register(ProductTopper)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetails)
