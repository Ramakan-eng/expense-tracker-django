from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from .models import Expense  
from .form import ExpenseForm
# Home Page
def home(request):
    return render(request, 'home.html')

# Signup Page
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'signup.html')


# Login Page
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('expense_list')  # redirect to dashboard
        else:
            messages.error(request, "Invalid username or password!")
    print(request.user.username)
    return render(request, 'login.html')


# Logout
def logout_user(request):
    auth_logout(request)
    return redirect('login')


# Expense List Page
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    total = sum(exp.amount for exp in expenses)
    return render(request, 'expense_list.html', {'expenses': expenses, 'total': total})


# Add Expense Page
from django.contrib.auth.decorators import login_required


@login_required
def add_expenses(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        
        category = request.POST.get('category')
        date = request.POST.get('date')

        if title and amount and category and date:
            Expense.objects.create(
                user=request.user,
                title=title,
                amount=amount,
                category=category,
                date=date
            )
            return redirect('expense_list')
        else:
            return render(request, 'add_expenses.html', {'error': 'All fields are required!'})

    return render(request, 'add_expenses.html')
