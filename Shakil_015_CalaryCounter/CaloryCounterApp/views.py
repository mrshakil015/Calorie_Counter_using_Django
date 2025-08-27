from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from datetime import date
from .models import *
from .forms import *

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')
        
        user_exists = AuthUserModel.objects.filter(username=username).exists()
        if user_exists:
            return redirect('register_view')
        else:
            if password == conf_password:
                user = AuthUserModel.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                
                if user:
                    UserProfileModel.objects.create(
                        user=user
                    )
                    return redirect('login_view')
                    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def dashboard(request):
    dailyconsumed_calorie_item = DailyConsumedCalorieModel.objects.all()
    total_consumed_data = TotalConsumedModel.objects.all()
    
    current_user = request.user
    gender = current_user.profile_user.Gender
    weight = current_user.profile_user.Weight
    height = current_user.profile_user.Height
    age = current_user.profile_user.Age
    
    today = date.today()
    
    today_consumed_calorie = TotalConsumedModel.objects.get(user=current_user, Date=today)
    
    if gender == 'Male':
        BMR = 66.47 + (13.75 * weight) + (5.003 * height)-(6.755 * age)
    else:
        BMR = 655.1 + (0.563 * weight) + (1.850 * height) - (4.676 * age)
    BMR = round(BMR,2)
    
    remaining = BMR - today_consumed_calorie.Total_calorie
    context = {
        'dailyconsumed_calorie_item':dailyconsumed_calorie_item,
        'total_consumed_data':total_consumed_data,
        'BMR': BMR,
        'today_consumed_calorie': today_consumed_calorie,
        'remaining': remaining,
    }
    
    return render(request, 'dashboard.html',context)

def profile_view(request):
    
    
    return render(request,'profile.html')

def profile_update(request):
    current_user = request.user
    user_data = UserProfileModel.objects.get(user = current_user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_data)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile_view')
    else:
        profile_form = UserProfileForm(instance=user_data)
        
    context = {
        'profile_form': profile_form
    }
    
    return render(request, 'profile_update.html', context)

def add_calorie(request):
    if request.method == 'POST':
        calorie_form = DailyConsumedCalorieForm(request.POST)
        if calorie_form.is_valid():
            calorie_form = calorie_form.save(commit=False)
            calorie_form.user = request.user
            calorie_form.save()
            
            date = calorie_form.Date
            
            calorie_data = TotalConsumedModel.objects.filter(user = request.user, Date = date).first()
            if calorie_data:
                calorie_data.Total_calorie += calorie_form.Calorie
                calorie_data.save()
            else:
                TotalConsumedModel.objects.create(
                    user = request.user,
                    Total_calorie = calorie_form.Calorie,
                    Date = date
                )
            return redirect('dashboard')
    else:
        calorie_form = DailyConsumedCalorieForm()
    context = {
        'calorie_form':calorie_form
    }
    
    return render(request, 'add-calorie.html',context)

def update_calorie(request, pk):
    calorie_data = DailyConsumedCalorieModel.objects.get(id=pk)
    old_calorie = calorie_data.Calorie
    
    if request.method == 'POST':
        calorie_form = DailyConsumedCalorieForm(request.POST, instance=calorie_data)
        if calorie_form.is_valid():
            calorie_form = calorie_form.save()
            
            date = calorie_form.Date
            
            calorie_data = TotalConsumedModel.objects.filter(user = request.user, Date = date).first()
            if calorie_data:
                calorie_data.Total_calorie -= old_calorie
                calorie_data.save()
                
                calorie_data.Total_calorie += calorie_form.Calorie
                calorie_data.save()
            else:
                TotalConsumedModel.objects.create(
                    user = request.user,
                    Total_calorie = calorie_form.Calorie,
                    Date = date
                )
            return redirect('dashboard')
    else:
        calorie_form = DailyConsumedCalorieForm(instance=calorie_data)
    context = {
        'calorie_form':calorie_form
    }
    
    return render(request, 'update-calorie.html',context)

def delete_calorie(request, pk):
    calorie_data = DailyConsumedCalorieModel.objects.get(id=pk)
    old_calorie = calorie_data.Calorie
    
    total_consumed_data = TotalConsumedModel.objects.filter(user=request.user, Date=calorie_data.Date).first()
    if total_consumed_data:
        total_consumed_data.Total_calorie -= old_calorie
        total_consumed_data.save()
    calorie_data.delete()
    return redirect('dashboard')

def logout_view(request):
    logout(request)
    return redirect('login_view')
    