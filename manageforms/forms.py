from django import forms
from .models import StaffDetails

class StaffForm(forms.ModelForm):
    class Meta:
        model = StaffDetails
        fields = ['name', 'job', 'email', 'permission', 'permission_to_add', 'permission_to_delete']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم الموظف'}),
            'job': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'العمل'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'الإيميل'}),
            'permission': forms.Select(attrs={'class': 'form-control'}),
            'permission_to_add': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'صلاحية تحتاج إضافة'}),
            'permission_to_delete': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'صلاحية تحتاج حذف'}),
        }
        labels = {
            'name': 'اسم الموظف',
            'job': 'العمل',
            'email': 'الإيميل المستخدم في النظام',
            'permission': 'الصلاحية',
            'permission_to_add': 'صلاحية تحتاج إلى إضافة',
            'permission_to_delete': 'صلاحية تحتاج إلى حذف',
        }

