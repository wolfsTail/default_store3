from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login, get_user_model
from django.contrib.auth.decorators import login_required
from django_email_verification import send_email
from django.contrib import messages

from .forms import UserCreateForm, LoginForm, UserUpdateForm


User = get_user_model()

def register_user(requset):
    context = {}
    if requset.method == 'POST':
        form = UserCreateForm(requset.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data['email']
            user_name = form.cleaned_data['username']
            user_password = form.cleaned_data['password1']
            user = User.objects.create_user(
                username=user_name, email=user_email, password=user_password
            )
            user.is_active = False
            send_email(user)            
            return redirect('account:email-verification-sent')
    else:
        form = UserCreateForm()
        context['form'] = form
    return render(requset, 'account/registration/register.html', context)

def login_user(request):
    context = {}

    if request.user.is_authenticated:
        return redirect('shop:products')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('account:dashboard')
        else:
            messages.info(request, 'Введены неверные данные!')
            return redirect('account:login')
        
    form = LoginForm()
    context['form'] = form
    return render(request, 'account/login/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('shop:products')

@login_required(login_url='account:login')
def dashboard_user(request):
    return render(request, 'account/dashboard/dashboard.html')

@login_required(login_url='account:login')
def profile_management(request):
    context = {}

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()          
            return redirect('account:dashboard')
    else:
        form = UserUpdateForm(instance=request.user)

    context['form'] = form
    return render(request, 'account/profile/profile-management.html')

@login_required(login_url='account:login')
def delete_user(request):
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        request.user.delete()
        return redirect('shop:products')
    
    return render(request, 'account/profile/account-delete.html')
