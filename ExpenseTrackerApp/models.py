from django.db import models
import datetime


# Create your models here.

class Expense(models.Model):

    category_choices = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Groceries', 'Groceries'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
        ('Health','Health'),
        ('Rent', 'Rent'),
        ('Other', 'Other'),
    ]

    expense_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100,error_messages={
            'max_length': 'Description must not exceed 100 characters.'
        } ,blank=False, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False,error_messages={
            'required': 'Amount is required',
            'max_length':'Amount is too long'
        } )
    category = models.CharField(max_length=50, blank=False, null=False, choices=category_choices,error_messages={
        'required':"Please Select A Category"
    })
    date = models.DateField(default=datetime.date.today, blank=False, null=False,error_messages={
        'required':'Expense Date Cannot be Blank'
    })

    def __str__(self):
        return f"{self.description} - {self.amount} on {self.date}"
    
    
    @classmethod
    def retrieve_expense(cls, start_date, end_date):
        return cls.objects.filter(date__range=[start_date, end_date])

    class Meta:
        ordering = ['-date']

    