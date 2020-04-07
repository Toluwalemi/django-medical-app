from django.contrib import admin

from pages.models import Patient, Practitioner, MedicalInfo, Illness


# Register your models here.


class PatientAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Patient, PatientAdmin)


class PractitionerAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Practitioner, PractitionerAdmin)


class MedicalInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'illness']


admin.site.register(MedicalInfo, MedicalInfoAdmin)

admin.site.register(Illness)
