from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
# Create your views here.

from Home.models import Profiling
from billing.models import *

def order_items(request, parent_id):
   #order_obj = Order.objects.get(order_id=parent_id)
   try:
      order_obj = Order.objects.get(order_id=parent_id)
   except Order.DoesNotExist:
      return render(request, '404.html')
   
   if request.method == 'POST' :
      prod_desc = request.POST['desc']
      unit_price =int(request.POST['unit_price'])
      quantity = int(request.POST['quantity'])
      total_amount =float(request.POST['amount'])
      orderProd = OrderItems.objects.create(itemOrder=order_obj, description=prod_desc, amount=total_amount, quantity=quantity, unit_price=unit_price)
      orderProd.save()
      messages.success(request, 'Order Placed:')   
      return redirect('order_items', parent_id=parent_id)
    
   items = OrderItems.objects.filter(itemOrder=order_obj)       
        # Getting The Orders data fetched:
   return render(request, 'Bills/order_prod_items.html', {"order_id": order_obj, 'items':items})   
    
def order_Products(request):
    if request.method == 'POST':
       customId = request.POST['customer_id']
       address = request.POST['address']
       billDate = request.POST['bill_date']
       dueDate = request.POST['due_date']
       pay_status = request.POST['status']
       price = int(request.POST['total_amount'])
    
    #* Getting the customer Id retrieved from the Profiling Model.  
       custom_id = Profiling.objects.get(user=customId)

    #*   Saving the data in the Table.
       Order.objects.create(customer=custom_id, address=address, bill_date=billDate, due_date=dueDate, status=pay_status, total_amount=price)
       messages.success(request, 'Saved Product Successfully:')
    
    #* Retrieving the Data of the User who is logged In:
    customs = Profiling.objects.filter(user=request.user)

    return render(request, 'Bills/order_prod.html' , {"customers": customs})


def prod_history(request):
    #* Retrieving the Data
    params = Order.objects.all()
    context = {
        'params':params
    }
    return render(request, 'Bills/Order_history.html', context)
 
def bill_terminal(request, order_Id):
   orderId = Order.objects.get(order_id=order_Id)
   items_list = OrderItems.objects.filter(itemOrder=order_Id)
   total_price = 0
   for item in items_list: 
         total_price = item.amount + total_price
         
   print(f'Total Amount{total_price}')
   if request.method == 'POST':
      reference_number = request.POST.get('reference')
      payment_date = request.POST.get('date')
      payment_method = request.POST.get('payment_method')
      bill_object = Payment.objects.create(bill=orderId, payment_date=payment_date, reference_number=reference_number, amount=total_price, payment_method=payment_method, payment_status='Paid')
      bill_object.save()
      return HttpResponse('Bill is saved:')
   return render(request, 'Bills/bill_payment.html', {'order':orderId, 'total_amount':total_price, 'orderItems':items_list})   