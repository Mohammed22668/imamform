from django.contrib import admin
from .models import FormDepartment, StaffDetails

@admin.register(FormDepartment)
class FormDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'governorate', 'manager_name', 'manager_email', 'manager_phone', 'created_at')
    list_filter = ('created_at', 'governorate')
    search_fields = ('name', 'governorate', 'manager_name', 'manager_email', 'manager_phone')

@admin.register(StaffDetails)
class StaffDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'job', 'email', 'permission', 'department')
    list_filter = ('permission', 'department')
    search_fields = ('name', 'email', 'job')


# @IMAM#2025#db
