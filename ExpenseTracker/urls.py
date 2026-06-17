"""
URL configuration for ExpenseTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from ExpenseTrackerApp import views
#from userlogin import views as user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.redirectlogin,name='first'),
    path('expenses/', views.index, name='index'),
    path('userlogin/',include('userlogin.urls',namespace='userlogin')),
    path('add-expense/', views.add_expense, name='add_expense'),    
    path('filter/', views.search_expenses_withpagination, name='search_expenses'),
    path('list/', views.expense_list, name='expense_list'),
    path('monthlyreport/', views.view_monthly_report, name='monthly_report'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('export_monthly_csv/', views.export_monthly_report, name='export_monthly_report'),
    path('delete/<int:expense_id>/',views.delete_expense,name="delete_expense"),
    path('update/<int:expense_id>/',views.update_expense,name="update_expense"),
  #  path('login/', user_view.login_view, name='login'),    # Login page
  #  path('register/', views.register, name='register')
   # path('register/', user_view.register, name ='register'),
]


