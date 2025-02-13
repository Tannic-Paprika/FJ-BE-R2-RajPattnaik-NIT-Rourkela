from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from django.db.models import Sum,F
from django.db.models.functions import TruncMonth
from .models import *
from django.core.mail import send_mail
import openai
from django.conf import settings

@login_required
def home(request):
    incomes = IncomeSource.objects.filter(user=request.user)
    expenses = Expenses.objects.filter(user=request.user)
    transactions = Transactions.objects.filter(user=request.user)
    budget_goals = BudgetGoal.objects.filter(user=request.user)

    total_income = sum(income.amount for income in incomes)
    total_expenses = sum(expense.split_amount for expense in expenses)
    total_savings = total_income - total_expenses

    monthly_income = incomes.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    monthly_expenses = expenses.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum(F('amount') / F('shared_by'))).order_by('month')
    
    context = {
        'incomes': incomes,
        'expenses': expenses,
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_savings': total_savings,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'budget_goals': budget_goals,
    }

    return render(request, 'home.html', context)

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
def add_budget_goal(request):
    if request.method == 'POST':
        form = BudgetGoalForm(request.POST)
        if form.is_valid():
            budget_goal = form.save(commit=False)
            budget_goal.user = request.user
            budget_goal.save()
            return redirect('home')
    else:
        form = BudgetGoalForm()
    return render(request, 'budget_form.html', {'form': form})

@login_required
def edit_budget_goal(request, budget_goal_id):
    budget_goal = BudgetGoal.objects.get(id=budget_goal_id)
    if request.method == 'POST':
        form = BudgetGoalForm(request.POST, instance=budget_goal)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BudgetGoalForm(instance=budget_goal)
    return render(request, 'budget_form.html', {'form': form})

@login_required
def delete_budgetgoal(request, pk):
    budgetgoal = get_object_or_404(BudgetGoal, pk=pk, user=request.user)
    if request.method == "POST":
        budgetgoal.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'object': budgetgoal})

def check_budget_overrun(user):
    budget_goals = BudgetGoal.objects.filter(user=user)
    for goal in budget_goals:
        total_expenses = Expenses.objects.filter(user=user, category=goal.category).aggregate(total=Sum('amount'))['total']
        if total_expenses and total_expenses > goal.goal_amount:
            send_budget_overrun_notification(user.email, goal.category.category, goal.goal_amount, total_expenses)

def send_budget_overrun_notification(email, category, goal_amount, total_expenses):
    subject = 'Budget Overrun Notification'
    message = f'Your expenses for category {category} have exceeded the budget goal. \n\nBudget Goal: {goal_amount} \nTotal Expenses: {total_expenses}'
    send_mail(subject, message, 'tannicpaprika@gmail.com', [email])

@login_required
def financial_advice(request):
    # Gather user's financial data here
    user = request.user
    # Fetch user's financial data from the database (e.g., incomes, expenses, etc.)

    # Prepare financial data to send to ChatGPT
    # This is just an example prompt, you can adjust it based on your needs
    prompt = f"User: {user.username}. Financial data: ..."
    
    # Generate advice from ChatGPT
    openai.api_key = settings.OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    advice = response.choices[0].text.strip()

    # Render the financial advice template with the advice
    return render(request, 'financial_advice.html', {'advice': advice})

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
 