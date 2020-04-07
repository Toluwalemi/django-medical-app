from django.contrib import admin

# Register your models here.

from pages.models import Patient, Practitioner


class PatientAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Patient, PatientAdmin)


class PractitionerAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Practitioner, PractitionerAdmin)
