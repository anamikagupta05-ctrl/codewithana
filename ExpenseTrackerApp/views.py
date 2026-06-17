#from unicodedata import category

from sqlite3 import Date

from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from ExpenseTrackerApp.forms import ExpenseForm
from ExpenseTrackerApp.models import Expense
from django.db.models import Sum
from .models import Expense
from django.contrib import messages
from django.db.models.functions import ExtractMonth
from django.utils.dates import MONTHS
from django.core.paginator import Paginator

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

# Requires the user to explicitly have the 'change_article' flag
#@permission_required('blog.change_article', raise_exception=True)
# Create your views here.



#default page
def redirectlogin(request):
    return redirect('userlogin/login')

@login_required(login_url='login/')
def index(request):
    print("inside index")
    return render(request, 'index.html')

@login_required(login_url='login/')
def add_expense(request):
    # Logic to handle adding an expense will go here
    if request.method == 'POST':
        # Process the form data and save the expense
         form = ExpenseForm(request.POST)
        # check whether it's valid:
         if form.is_valid():
            form.save()
            messages.success(request,"Thanks Data Successfully Entered")
            return render(request, 'index.html')
        # If the form was invalid send the user back to fix it
         else:
             return render(request, 'index.html')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ExpenseForm()        
    return render(request, 'add_expense.html', {'form': form})

@login_required(login_url='login/')
def delete_expense(request, expense_id):
    # Logic to handle deleting an expense will go here
    expense = Expense.objects.get(expense_id=expense_id)
    expense.delete()
    messages.success(request,"Data Successfully Deleted")
    return render(request, 'index.html')

def update_expense(request,expense_id):

    #render update html page
    if request.method=='POST':
        # Process the form data and save the expense
         form = ExpenseForm(request.POST)
        # check whether it's valid:
         if form.is_valid():
            form.save()
            messages.success(request,"Thanks Data Successfully Updated")
            return render(request, 'index.html')
        
    else:
        expense=Expense.objects.get(expense_id=expense_id)
        if expense:
            form=ExpenseForm(instance=expense)
        else:
            messages.error('request',"No Record Found")


    return render(request,'update_expense.html',{'form':form,'expense_id':expense_id})
   
     
@login_required(login_url='login/')
def expense_list(request):
    
    # Logic to handle listing expenses will go here
    
    expense_list = Expense.objects.all().order_by('-date').values()
    expense_paginator=Paginator(expense_list,10)

    page_number = request.GET.get("page")
    page_obj = expense_paginator.get_page(page_number)

    total=round(sum(expense['amount'] for expense in expense_list))
    
    return render(request, 'expense_list.html', {'expense_list':page_obj , 'total': total})

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def parse_csvdate(date_str):
    try:
        date_str=datetime.strptime(date_str, "%B %d, %Y").date()
        date_str=date_str.strftime("%Y-%m-%d")
  
        return date_str
    except ValueError:
        return None


def expense_dailychart(start_date, end_date, selected_category):

    daily_data = (
        Expense.objects.filter(date__range=[start_date,end_date])
        .values('date')
        .annotate(total=Sum('amount')).order_by('category'))
   
    if selected_category:
       daily_data = daily_data.filter(category=selected_category)

    daily_labels = [item['date'].isoformat() for item in daily_data]
    daily_data = [round(float(item['total']),2) for item in daily_data]

    return daily_labels, daily_data


def search_expenses(request):

    # Logic to handle searching expenses will go here
    if request.method == 'POST':

            start_date = (request.POST.get('start_date') or "" ).strip()
            end_date =(request.POST.get('end_date') or "").strip()
            category = (request.POST.get('category') or "").strip()

            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            selected_category = category
            
            total_filtered=0

            cat_choices=[]
            
            for value, label in Expense.category_choices:
                cat_choices.append({
                "value": value,
                "label": label,
                "selected": value == selected_category
            })
                   
            if start_date and end_date and end_date < start_date:
            # raise ValueError("End date must be after start date.")  
                messages.error(request, "End date must be after start date.")

                return render(request, 'expense_report.html', {'cat_choices': cat_choices,
                                                            start_date: start_date, 'end_date': end_date, 'selected_category': selected_category,    
                                                                'total_filtered': total_filtered})  
            elif start_date and end_date and category:
                expenses = Expense.objects.filter(
                    date__range=[start_date, end_date] , category=category).order_by('-date') 
                total_filtered=round(expenses.aggregate(Sum('amount'))['amount__sum'] or 0,2)    
            else:
                expenses = Expense.objects.filter(
                    date__range=[start_date, end_date]).order_by('-date')
                total_filtered=round(expenses.aggregate(Sum('amount'))['amount__sum'] or 0,2) 

            # chart 

            daily_labels, daily_data = expense_dailychart(start_date, end_date, selected_category)

            category_data = (Expense.objects.values('category').annotate(total=Sum('amount')))
  
            if start_date and end_date and selected_category:
                category_data = (
            Expense.objects.filter(date__range=[start_date, end_date] , category=selected_category)
            .values('category')
            .annotate(total=Sum('amount'))
                )
            else:         
                 category_data = (
            Expense.objects.filter(date__range=[start_date, end_date])
            .values('category')
            .annotate(total=Sum('amount')))
    
            category_labels, category_data = load_piechart_data(category_data) 
            expense_paginator=Paginator(expenses,5)

            page_number = request.GET.get("page")
            page_obj = expense_paginator.get_page(page_number)
        
            return render(request, 'expense_report.html', {'expenses_filtered': page_obj,'selected_category': selected_category,
                                                            'start_date': start_date, 'end_date': end_date,
                                                                'cat_choices': cat_choices, 'total_filtered': total_filtered,
                                                                'category_labels': category_labels, 
                                                                'category_data': category_data,
                                                                'daily_labels': daily_labels,
                                                            'daily_data': daily_data})
    else:


        cat_choices = [{'value': value, 'label': label, 'selected': False} for value, label in Expense.category_choices]    
        total_filtered=0
            
    return render(request, 'expense_report.html', {'cat_choices': cat_choices,
                                                    'total_filtered': total_filtered})
                                                      #'selected_category': selected_category,
                                                      #'start_date': start_date, 'end_date': end_date})


def export_csv(request):
             
    start = (request.GET.get('start') or "" ).strip()
    end =(request.GET.get('end') or "").strip()
    category = (request.GET.get('selected_category') or "").strip()

    start = parse_csvdate(start)
    end = parse_csvdate(end)

    
    # Logic to handle exporting expenses to CSV will go here
    if start and end and category :
         expenses = Expense.objects.filter(date__range=[start, end], category=category).order_by('-date').values()
    else:
         expenses = Expense.objects.filter(date__range=[start, end]).order_by('-date').values()

    fname_start=start or "all"
    fname_end=end or "all"
    file_name=f"expenses_{fname_start}_{fname_end}.csv"

    row=create_csv(expenses)
    
    csv_data = '\n'.join(row)

    return HttpResponse(csv_data, content_type='text/csv',
                         headers={'Content-Disposition': f'attachment; filename="{file_name}"'})

#method of monthly report
def view_monthly_report(request):
    # Logic to handle viewing monthly report will go here

    if request.method == 'POST':
        report_month = request.POST.get('report_month')
    else :
        report_month=Date.today().month

   
    month_list=[{"value": month_num, "label": month_name, "selected": month_num == int(report_month)} for month_num, month_name in MONTHS.items()]

    expenses=Expense.objects.filter(date__month=report_month).order_by('-date').values()

    expenses_piechart=expenses.annotate(month=ExtractMonth('date')).values('category').annotate(total=Sum('amount')).order_by('category')

    if expenses_piechart:
        category_labels,category_data=load_piechart_data(expenses_piechart)
    else :
        category_data=[]
        category_labels=[]

    return render(request, 'monthly_report.html', {'expenses': expenses, 'month_list': month_list, 
                                                   'category_data':category_data,'category_labels':category_labels,'report_month': report_month})


def create_csv(expenses)-> list:

    row=["Date,Category,Amount,Description\n"]
    for expense in expenses:
        row.append(f"{expense['date'].isoformat()},{expense['category']},{expense['amount']},{expense['description']}\n")
    return row

def export_monthly_report(request):

    month=request.GET.get("month")

    if month:
        expenses=Expense.objects.filter(date__month=month).order_by('-date').values()

    row=create_csv(expenses)

    csv_data = '\n'.join(row)

    file_name=f"expenses_{month}.csv"

    return HttpResponse(csv_data, content_type='text/csv',
                         headers={'Content-Disposition': f'attachment; filename="{file_name}"'})
    
    

def load_piechart_data(expense):

    category_labels=[]
    category_data=[]
    for item in expense:
        category_labels.append(item['category'])
        category_data.append(round(float(item['total']),2)) 

    return category_labels,category_data


def search_expenses_withpagination(request):

    # Logic to handle searching expenses will go here
    #

    #when get and post both have start_date 

    flag=(request.method== 'GET' and request.GET.get('start_date') is not None) or (request.method=='POST' and request.POST.get('start_date') is not None)
    
    if flag: 
        
        if request.method == 'POST':
            start_date = (request.POST.get('start_date')) 
            end_date =(request.POST.get('end_date'))  
            category = (request.POST.get('category')) 
        else :

            start_date=request.GET.get('start_date')
            end_date=request.GET.get('end_date')
            category=request.GET.get('category')

        
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        selected_category = category
                
        total_filtered=0

        cat_choices=[]
                
        for value, label in Expense.category_choices:
            cat_choices.append({
                    "value": value,
                    "label": label,
                    "selected": value == selected_category})

        

        if start_date and end_date and end_date < start_date:
                # raise ValueError("End date must be after start date.")  
            messages.error(request, "End date must be after start date.")

            return render(request, 'expense_report.html', {'cat_choices': cat_choices,
                                                                start_date: start_date, 'end_date': end_date, 'selected_category': selected_category,    
                                                                    'total_filtered': total_filtered})  
        elif start_date and end_date and category:
            expenses = Expense.objects.filter(
                        date__range=[start_date, end_date] , category=category).order_by('-date') 
            total_filtered=round(expenses.aggregate(Sum('amount'))['amount__sum'] or 0,2)    
        else:
            expenses = Expense.objects.filter(
                        date__range=[start_date, end_date]).order_by('-date')
            total_filtered=round(expenses.aggregate(Sum('amount'))['amount__sum'] or 0,2) 

                # chart 

        daily_labels, daily_data = expense_dailychart(start_date, end_date, selected_category)

        if start_date and end_date and selected_category:
            category_data = (
                Expense.objects.filter(date__range=[start_date, end_date] , category=selected_category)
                .values('category')
                .annotate(total=Sum('amount'))
                    )
        else:         
            category_data = (
                Expense.objects.filter(date__range=[start_date, end_date])
                .values('category')
                .annotate(total=Sum('amount')))
        
        category_labels, category_data = load_piechart_data(category_data) 
                #expense_piechart(start_date, end_date, selected_category)
                

        expense_paginator=Paginator(expenses,5)

        page_number = request.GET.get("page")
        page_obj = expense_paginator.get_page(page_number)
        
        
        return render(request, 'expense_report.html', {'expenses_filtered': page_obj,'selected_category': selected_category,
                                                                'start_date': start_date, 'end_date': end_date,
                                                                    'cat_choices': cat_choices, 'total_filtered': total_filtered,
                                                                    'category_labels': category_labels, 
                                                                    'category_data': category_data,
                                                                    'daily_labels': daily_labels,
                                                                'daily_data': daily_data})
        
    else :
      
        cat_choices = [{'value': value, 'label': label, 'selected': False} for value, label in Expense.category_choices]    
        total_filtered=0
            
        return render(request, 'expense_report.html', {'cat_choices': cat_choices,
                                                    'total_filtered': total_filtered})

