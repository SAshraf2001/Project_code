from django.urls import path
from Reports import views
urlpatterns = [
     path('report-module/', views.report_type, name='reportType'),
     path('report/', views.report, name='Report')
]
