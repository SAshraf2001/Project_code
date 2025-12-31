from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from Home.models import Profiling
from billing.models import Order, OrderItems, Payment
from django.utils import timezone

def order_items(request, parent_id): #* 4 --> lineTotal = 23400 Actually debugging how the product is being saved in the ordered_items model accordingly.
   try:
      order_obj = Order.objects.get(order_id=parent_id)
   except Order.DoesNotExist:
      return render(request, '404.html')

   unit_price =0
   lineTotal = 0
   if request.method == 'POST' :
      prod_desc = request.POST['desc']
      quantity = int(request.POST['quantity'])
      unit_price = int(request.POST.get('unit_price'))
      lineTotal = unit_price * quantity
      print(f'The total Price of the Ordered Product is:{lineTotal}')
  
      orderProd = OrderItems.objects.create(itemOrder=order_obj, description=prod_desc, amount=lineTotal, quantity=quantity, unit_price=unit_price)
      orderProd.save()
      messages.success(request, 'Order Placed:')   
      return redirect('bill_Terminal', order_Id=parent_id)
    
   items = OrderItems.objects.filter(itemOrder=order_obj)       
        # Getting The Orders data fetched:
   return render(request, 'Bills/order_prod_items.html', {"order_id": order_obj, 'items':items, 'amount':unit_price})   
    
def order_Products(request):
     #* Retrieving the Data of the User who is logged In:
    customs = Profiling.objects.filter(user=request.user)
    if request.method == 'POST':
       customId = request.POST['customer_id']
       address = request.POST['address']
       billDate = request.POST['bill_date']
       dueDate = request.POST['due_date']
       pay_status = request.POST['status']
    
    #* Getting the customer Id retrieved from the Profiling Model.  
       try:
         custom_id = Profiling.objects.get(user=customId) #* 4 --> Generated from here then going to the order_item function where the rest of the work is bieng done. Customer is coming from the cusomter foreign key being used for fetching the user's data.
       except Profiling.DoesNotExist:
         return render(request, '404.html')


    #*   Saving the data in the Table.
       Order.objects.create(customer=custom_id, address=address, bill_date=billDate, due_date=dueDate, status=pay_status)
       messages.success(request, 'Saved Product Successfully:')
       return redirect('prod_History')

    return render(request, 'Bills/order_prod.html' , {"customers": customs})


def prod_history(request):
    #* Retrieving the Data
   # params = Order.objects.all()
    param_user = Profiling.objects.get(user=request.user)
    param_user_a = Order.objects.filter(customer=param_user)
    #* Fetching the Data from the OrderItems against the same ID:
    
    for order in param_user_a:
       total = 0
       sum_total = 0
       order_object = OrderItems.objects.filter(itemOrder = order)
       for item in order_object:
          total = item.amount + total
       sum_total += total
       order.total_amount = sum_total
    context = {
        'params':param_user_a,
    }
    return render(request, 'Bills/Order_history.html', context)
 
def bill_terminal(request, order_Id):
   try:
      orderId = Order.objects.get(order_id=order_Id)
   except Order.DoesNotExist:
      return render(request, '404.html')
   items_list = OrderItems.objects.filter(itemOrder=order_Id)
   total_price = 0
   for item in items_list: 
         total_price = item.amount + total_price
   if request.method == 'POST':
      reference_number = request.POST.get('reference')
      payment_date = request.POST.get('date') or timezone.now()
      payment_method = request.POST.get('payment_method')
      bill_object = Payment.objects.create(bill=orderId, payment_date=payment_date, reference_number=reference_number, amount=total_price, payment_method=payment_method, payment_status='Paid')
      bill_object.save()
      return redirect('Payment_Confirmed')
   return render(request, 'Bills/bill_payment.html', {'order':orderId, 'total_amount':total_price, 'orderItems':items_list})   

def payment_confirmed(request):
   latest_payment = Payment.objects.latest('payment_date').last()
   params = OrderItems.objects.filter(itemOrder=latest_payment.bill)
   print(latest_payment)
   context = {"param":params,
              'latest_payment':latest_payment, 
              'total':latest_payment.amount}
   return render(request, 'Bills/payment_confirmed.html', context)