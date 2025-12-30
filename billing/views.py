from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from Home.models import Profiling
from billing.models import Order, OrderItems, Payment

def order_items(request, parent_id):
   try:
      order_obj = Order.objects.get(order_id=parent_id)
   except Order.DoesNotExist:
      return render(request, '404.html')

   unit_price =0
   lineTotal = 0
   unitPrice = Order.objects.filter(order_id=parent_id)
   for item in unitPrice:
        unit_price = item.total_amount
        
   if request.method == 'POST' :
      prod_desc = request.POST['desc']
      quantity = int(request.POST['quantity'])
      lineTotal = unit_price * quantity
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
       price = float(request.POST['total_amount'])
    
    #* Getting the customer Id retrieved from the Profiling Model.  
       custom_id = Profiling.objects.get(user=customId)


    #*   Saving the data in the Table.
       Order.objects.create(customer=custom_id, address=address, bill_date=billDate, due_date=dueDate, status=pay_status, total_amount=price)
       messages.success(request, 'Saved Product Successfully:')
       return redirect('prod_History')

    return render(request, 'Bills/order_prod.html' , {"customers": customs})


def prod_history(request):
    #* Retrieving the Data
   # params = Order.objects.all()
    param_user = Profiling.objects.get(user=request.user)
    param_user_a = Order.objects.filter(customer=param_user)
    
   # print(param_user_a)
    context = {
        'params':param_user_a
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
      payment_date = request.POST.get('date')
      payment_method = request.POST.get('payment_method')
      bill_object = Payment.objects.create(bill=orderId, payment_date=payment_date, reference_number=reference_number, amount=total_price, payment_method=payment_method, payment_status='Paid')
      bill_object.save()
      return redirect('Payment_Confirmed')
   return render(request, 'Bills/bill_payment.html', {'order':orderId, 'total_amount':total_price, 'orderItems':items_list})   

def payment_confirmed(request):
   params = Payment.objects.all()
   context = {"param":params}
   return render(request, 'Bills/payment_confirmed.html', context)