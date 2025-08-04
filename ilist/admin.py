from django.contrib import admin

from ilist.models import Status, Todo
# Register your models here.
admin.site.register((Status, Todo))