from django.urls import path
from Reports import views
urlpatterns = [
     path('', views.home_index, name='home_Index')
]
