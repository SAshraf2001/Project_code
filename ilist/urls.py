from django.contrib import admin

from django.urls import path

from ilist import views

urlpatterns = [
    path('home_todo', views.content, name='content'),
    path('viewTodo', views.displayTodo, name='displayTodo')
]
