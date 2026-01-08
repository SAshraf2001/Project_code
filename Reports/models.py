from django.db import models
import secrets
import string

# Create your models here.

def random_ids():
    prefix = ''.join(secrets.choice(string.ascii_lowercase) for _ in range(3))

    suffix = ''.join(secrets.choice(string.digits) for _ in range(4))

    return f"{prefix}-{suffix}"
class ReportType(models.Model):
    reportType = models.CharField(primary_key=True, default=random_ids, null=False, blank=False, max_length=22)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=False, null=False)
    
    def __str__(self):
        return f'{self.reportType} - {self.name}'
    
class Report(models.Model):
    report_id = models.CharField(primary_key=True,  max_length= 22, default=random_ids, blank=False, null=False)
    report_type = models.ForeignKey(ReportType, related_name='reports', on_delete=models.CASCADE)
    generated_by = models.CharField(max_length=233)
    generated_at = models.DateTimeField(auto_now_add=True)
    parameters = models.TextField(blank=True, null=True)
    file_path = models.FileField(upload_to='reports_pdf/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.report_id} - {self.report_type.name}"