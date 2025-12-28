from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('users/', views.all_users, name='all_users'),
    path('person/', views.user, name='user'),
    path('login/', views.loginAccount, name='login'), 
    path('signup/', views.signup, name='signup'),
    path('logout/', views.handle_logout, name='logout')
]