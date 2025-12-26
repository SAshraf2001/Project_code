from django.contrib import admin

# Register your models here.
from billing.models import *
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Payment)