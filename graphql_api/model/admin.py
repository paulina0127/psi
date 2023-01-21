from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Commodity)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Basket)
admin.site.register(Pay)
