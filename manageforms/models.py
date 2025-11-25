from django.db import models

# Create your models here.


class FormDepartment(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم القسم")
    governorate = models.CharField(max_length=255, verbose_name="المحافظة")
    manager_name = models.CharField(max_length=255, verbose_name="اسم مدير أو رئيس القسم")
    manager_email = models.EmailField(max_length=255, blank=True, verbose_name="إيميل رئيس القسم")
    manager_phone = models.CharField(max_length=20, blank=True, verbose_name="رقم هاتف رئيس القسم")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "قسم الاستمارة"
        verbose_name_plural = "أقسام الاستمارات"


class StaffDetails(models.Model):
    PERMISSION_CHOICES = [
        ('admin', 'مدير'),
        ('user', 'مستخدم'),
        ('viewer', 'مشاهد'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="اسم الموظف")
    job = models.CharField(max_length=255, verbose_name="العمل")
    email = models.EmailField(max_length=255, verbose_name="الإيميل المستخدم في النظام")
    permission = models.CharField(max_length=50, choices=PERMISSION_CHOICES, default='user', verbose_name="الصلاحية")
    permission_to_add = models.CharField(max_length=255, blank=True, verbose_name="صلاحية تحتاج إلى إضافة")
    permission_to_delete = models.CharField(max_length=255, blank=True, verbose_name="صلاحية تحتاج إلى حذف")
    department = models.ForeignKey(FormDepartment, on_delete=models.CASCADE, verbose_name="القسم")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "تفاصيل الموظف"
        verbose_name_plural = "تفاصيل الموظفين"


