from django.contrib import admin
from docking.models import Receptor, Docking

class ReceptorAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'name')
    
admin.site.register(Receptor, ReceptorAdmin)

class DockingAdmin(admin.ModelAdmin):
    list_display = ('uniquestring', 'id', 'molname')
    
admin.site.register(Docking, DockingAdmin)