from django.shortcuts import render, redirect
from django.http import HttpResponse
from Reports.models import Report, ReportType
from Home.models import Profiling
from django.contrib import messages
# Create your views here.

from billing.models import Payment
from Home.models import Profiling

def report_type(request):
    params = ReportType.objects.all()
    history = Report.objects.filter(generated_by=request.user.username).order_by('-generated_at')
    
    context = {
        'params': params,
        'reports': history
    }
    if request.method == 'POST':
        selected_type_id = request.POST.get('report_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        type_instance = ReportType.objects.get(reportType=selected_type_id)
        
        param = f'Start Date {start_date} to End Date {end_date} | Amount Spent'
        try:
            # We use request.user (the object) which Django handles automatically
            profile = Profiling.objects.get(user=request.user)
            username_str = profile.username
        except (Profiling.DoesNotExist, AttributeError):
            # Fallback if profile is missing
            username_str = request.user.username
        
        Report.objects.create(report_type=type_instance, generated_by=username_str, parameters=param)
    return render(request, 'Report/report_module.html', context)


def report(request):
    if request.method == 'POST':
        name= request.POST.get('name')
        description = request.POST.get('description')
        ReportType.objects.create(name=name, description=description)
        messages.success(request, 'Your Report has been saved successfully:')
        return redirect('Report')
    
    params = ReportType.objects.all()
    context = {'params':params}
    return render(request, 'Report/reports.html', context) 