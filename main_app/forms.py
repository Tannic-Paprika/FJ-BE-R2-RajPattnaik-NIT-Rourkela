from django import forms
from .models import *

class IncomeSourceForm(forms.ModelForm):
    class Meta:
        model = IncomeSource
        fields = ['description', 'date', 'amount']

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['category', 'amount']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['description', 'date', 'amount']
