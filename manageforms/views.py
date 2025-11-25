from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FormDepartment, StaffDetails
from django.forms import modelformset_factory
from django.views.decorators.csrf import ensure_csrf_cookie

# الصفحة الترحيبية
def home(request):
    return render(request, 'manageforms/home.html')

# صفحة الفورم
def form_page(request):
    StaffFormSet = modelformset_factory(StaffDetails, fields=('name', 'job', 'email', 'permission', 'permission_to_add', 'permission_to_delete'), extra=3, can_delete=True)
    
    if request.method == 'POST':
        # حفظ بيانات القسم
        department_name = request.POST.get('department_name')
        governorate = request.POST.get('governorate')
        manager_name = request.POST.get('manager_name')
        manager_email = request.POST.get('manager_email', '')
        manager_phone = request.POST.get('manager_phone', '')
        
        if department_name and governorate and manager_name:
            department = FormDepartment.objects.create(
                name=department_name,
                governorate=governorate,
                manager_name=manager_name,
                manager_email=manager_email,
                manager_phone=manager_phone
            )
            
            # حفظ بيانات الموظفين
            formset = StaffFormSet(request.POST, queryset=StaffDetails.objects.none())
            if formset.is_valid():
                for form in formset:
                    if form.has_changed() and not form.cleaned_data.get('DELETE', False):
                        staff = form.save(commit=False)
                        staff.department = department
                        staff.save()
                
                messages.success(request, 'تم حفظ البيانات بنجاح!')
                return redirect('form_page')
        else:
            messages.error(request, 'يرجى ملء جميع حقول القسم')
    
    formset = StaffFormSet(queryset=StaffDetails.objects.none())
    return render(request, 'manageforms/form.html', {'formset': formset})

# صفحة تسجيل الدخول
@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'يرجى إدخال اسم المستخدم وكلمة المرور')
            return render(request, 'manageforms/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    
    return render(request, 'manageforms/login.html')

# صفحة الداشبورد
@login_required
def dashboard(request):
    # إحصائيات سريعة
    total_departments = FormDepartment.objects.count()
    total_staff = StaffDetails.objects.count()
    recent_departments = FormDepartment.objects.all().order_by('-created_at')[:5]
    
    return render(request, 'manageforms/dashboard.html', {
        'total_departments': total_departments,
        'total_staff': total_staff,
        'recent_departments': recent_departments
    })

# تسجيل الخروج
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# صفحة عرض الطلبات (تتطلب تسجيل الدخول)
@login_required
def requests_list(request):
    departments = FormDepartment.objects.all().order_by('-created_at')
    
    # البحث
    search_query = request.GET.get('search', '')
    search_type = request.GET.get('search_type', 'all')
    
    if search_query:
        if search_type == 'name':
            departments = departments.filter(name__icontains=search_query)
        elif search_type == 'governorate':
            departments = departments.filter(governorate__icontains=search_query)
        elif search_type == 'manager':
            departments = departments.filter(manager_name__icontains=search_query)
        else:  # all
            departments = departments.filter(
                name__icontains=search_query
            ) | departments.filter(
                governorate__icontains=search_query
            ) | departments.filter(
                manager_name__icontains=search_query
            )
    
    return render(request, 'manageforms/requests_list.html', {
        'departments': departments,
        'search_query': search_query,
        'search_type': search_type
    })

# عرض تفاصيل طلب معين
@login_required
def request_detail(request, department_id):
    try:
        department = FormDepartment.objects.get(id=department_id)
        staff_members = StaffDetails.objects.filter(department=department)
        return render(request, 'manageforms/request_detail.html', {
            'department': department,
            'staff_members': staff_members
        })
    except FormDepartment.DoesNotExist:
        messages.error(request, 'الطلب المطلوب غير موجود')
        return redirect('requests_list')
