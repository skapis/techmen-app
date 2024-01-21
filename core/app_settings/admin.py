from django.contrib import admin
from .models import WorkItemDescription, WorkList


admin.site.register(WorkList)
admin.site.register(WorkItemDescription)
