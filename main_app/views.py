from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from .models import *

@login_required
def home(request):
    incomes = IncomeSource.objects.filter(user=request.user)
    expenses = Expenses.objects.filter(user=request.user)
    transactions = Transactions.objects.filter(user=request.user)

    return render(request, 'home.html', {
        'incomes': incomes,
        'expenses': expenses,
        'transactions': transactions,
    })

@login_required
def add_income(request):
    if request.method == "POST":
        form = IncomeSourceForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('home')
    else:
        form = IncomeSourceForm()
    return render(request, 'income_form.html', {'form': form})

@login_required
def edit_income(request, pk):
    income = get_object_or_404(IncomeSource, pk=pk, user=request.user)
    if request.method == "POST":
        form = IncomeSourceForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IncomeSourceForm(instance=income)
    return render(request, 'income_form.html', {'form': form})

@login_required
def delete_income(request, pk):
    income = get_object_or_404(IncomeSource, pk=pk, user=request.user)
    if request.method == "POST":
        income.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'object': income})

# Similarly, create views for ExpenseCategory and Transaction
@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseCategoryForm()
    return render(request, 'expense_form.html', {'form': form})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expenses, pk=pk, user=request.user)
    if request.method == "POST":
        form = ExpenseCategoryForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseCategoryForm(instance=expense)
    return render(request, 'expense_form.html', {'form': form})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expenses, pk=pk, user=request.user)
    if request.method == "POST":
        expense.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'object': expense})

@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('home')
    else:
        form = TransactionForm()
    return render(request, 'transaction_form.html', {'form': form})

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transactions, pk=pk, user=request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transaction_form.html', {'form': form})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transactions, pk=pk, user=request.user)
    if request.method == "POST":
        transaction.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'object': transaction})

@login_required
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/home/')

    return render(request, 'login.html')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()

        messages.info(request, "Account created Successfully!")
        return redirect('/login/')

    return render(request, 'register.html')
 