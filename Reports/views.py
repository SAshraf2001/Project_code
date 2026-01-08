from django.shortcuts import render, redirect
from django.http import HttpResponse
from Reports.models import Report, ReportType
from Home.models import Profiling
from billing.models import Order, OrderItems, Payment
from django.contrib import messages
from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Create your views here.

from billing.models import Payment
from Home.models import Profiling
def report_type(request):
    params = ReportType.objects.all()
    history = Report.objects.filter(generated_by=request.user.username).order_by('-generated_at')
    param = Report.objects.all()
    
    context = {'params': params, 'reports': history,'param':param}
    
    if request.method == 'POST':
        selected_type_id = request.POST.get('report_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        type_instance = ReportType.objects.get(reportType=selected_type_id)
        report_name = type_instance.name.lower() # To make comparison easy

        profile = None
        try:
            profile = Profiling.objects.get(user=request.user)
            username_str = profile.username
        except:
            username_str = request.user.username

        # --- REVENUE LOGIC (Matches 'Revenue Spent', 'Daily Revenue', etc.) ---
        if 'revenue' in report_name:
            order_qs = Order.objects.filter(customer=profile)
            id_fetched = []
            for items in order_qs:
                id_fetched.append(items.order_id)
            
            payment_qs = Payment.objects.filter(bill__in=id_fetched, payment_date__range=[start_date, end_date])
            amount = 0
            for items in payment_qs:
                amount = items.amount + amount
            
            param = f'Revenue Report | {start_date} to {end_date} | Total: {amount}'
            pdf_title = "Revenue Report"
            final_value = f"Total Revenue Spent: {amount}"

        # --- LOYALTY LOGIC (Matches 'Loyalty Points', 'Points Report', etc.) ---
        elif 'loyalty' in report_name:
            order_qs = Order.objects.filter(customer=profile)
            id_fetched = []
            for items in order_qs:
                id_fetched.append(items.order_id)
            
            payment_qs = Payment.objects.filter(bill__in=id_fetched, payment_date__range=[start_date, end_date])
            total_spent = 0
            for items in payment_qs:
                total_spent = total_spent + items.amount
            
            # Logic: 1 Point for every 10 units spent
            points = total_spent / 10
            param = f'Loyalty Report | {start_date} to {end_date} | Points Earned: {points}'
            pdf_title = "Loyalty Points Report"
            final_value = f"Total Points Earned: {points}"
            amount = points # To use in PDF

        else:
            return HttpResponse('Selected Column is wrong')

        # --- PDF GENERATION LOGIC ---
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setFont("Poppins-bold", 16)
        p.drawString(100, 750, pdf_title)
        p.setFont("Poppins", 12)
        p.drawString(100, 720, f"Customer: {username_str}")
        p.drawString(100, 700, f"Period: {start_date} to {end_date}")
        p.drawString(100, 680, final_value)
        p.showPage()
        p.save()
        buffer.seek(0)

        # Create Report and Save PDF
        new_report = Report.objects.create(
            report_type=type_instance, 
            generated_by=username_str, 
            parameters=param
        )
        new_report.file_path.save(f'report_{new_report.report_id}.pdf', ContentFile(buffer.read()))
        
        return redirect(request.path)

    return render(request, 'Report/report_module.html', context)
def report(request):
    if request.method == 'POST':
        name= request.POST.get('name')
        description = request.POST.get('description')
        ReportType.objects.create(name=name, description=description)
        messages.success(request, 'Your Report has been saved successfully:')
        return redirect('reportType')
    
    params = ReportType.objects.all()
    context = {'params':params}
    return render(request, 'Report/reports.html', context) 