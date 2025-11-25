from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('form/', views.form_page, name='form_page'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('requests/', views.requests_list, name='requests_list'),
    path('request/<int:department_id>/', views.request_detail, name='request_detail'),
]

