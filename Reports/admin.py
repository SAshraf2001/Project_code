from django.contrib import admin

# Register your models here.
from Reports.models import Report, ReportType

admin.site.register(Report)
admin.site.register(ReportType)