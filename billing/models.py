from django.db import models
from Home.models import Profiling

import string
import secrets

#defining a function for random Ids generation:
def random_ids():
    prefix = ''.join(secrets.choice(string.ascii_lowercase) for _ in range(3))

    suffix = ''.join(secrets.choice(string.digits) for _ in range(4))

    return f"{prefix}-{suffix}"

# Create your models here.
class Order(models.Model):
    order_id = models.CharField(max_length=23, primary_key=True, default=random_ids, editable=False)
    customer = models.ForeignKey(Profiling,  on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=100, null=False, blank=False)
    status = models.CharField(max_length=12, blank=False, null=False)
    bill_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
       return  f'{self.order_id}'

class OrderItems(models.Model):
    order_item_id = models.CharField(max_length=32, primary_key=True, default=random_ids, editable=False)
    itemOrder = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=230, null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    
    def __str__(self):
        return f'{self.description}'



class Payment(models.Model):
    payId = models.CharField(max_length=15, primary_key=True, default=random_ids, editable=False)
    bill= models.ForeignKey(Order, on_delete=models.CASCADE,  related_name='bills')
    payment_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=23, null=False, blank=False)
    reference_number = models.IntegerField()
    payment_status = models.CharField(max_length=14, null=False, blank=False)
    
    def __str__(self):
        return self.payId