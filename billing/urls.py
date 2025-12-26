from django.urls import path

from billing import views

urlpatterns = [
    path('order-items/<slug:parent_id>/', views.order_items, name='order_items'),
    path('prods/', views.order_Products, name='order_Products'),
    path('history/', views.prod_history, name='prod_History'),
    path('bill-terminal/<slug:order_Id>/', views.bill_terminal, name='bill_Terminal')
]