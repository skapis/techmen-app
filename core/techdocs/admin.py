from django.contrib import admin
from .models import ProductionLine, Record, MachineWorks, MachineIssues, Components, Variables, RecordSum

admin.site.register(ProductionLine)
admin.site.register(Record)
admin.site.register(MachineWorks)
admin.site.register(MachineIssues)
admin.site.register(Components)
admin.site.register(Variables)
admin.site.register(RecordSum)

