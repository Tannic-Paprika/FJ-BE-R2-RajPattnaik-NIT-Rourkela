from django import forms
from .models import *

class IncomeSourceForm(forms.ModelForm):
    class Meta:
        model = IncomeSource
        fields = ['description', 'date', 'amount']

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['category', 'amount','date','shared_by','receipt']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['description', 'date', 'amount']

class BudgetGoalForm(forms.ModelForm):
    class Meta:
        model = BudgetGoal
        fields = ['category', 'goal_amount',]

class FinancialAdviceForm(forms.Form):
    query = forms.CharField(widget=forms.Textarea, label="Your Question")
