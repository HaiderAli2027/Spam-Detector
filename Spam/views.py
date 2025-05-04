from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
import os
import joblib
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Load models
model1 = joblib.load(os.path.dirname(__file__) + "\\mySVCModel1.pk1")
model2 = joblib.load(os.path.dirname(__file__) + "\\myModel1.pk1")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def default_view(request):
    if 'authdetails' in request.session:
        return redirect('Index') 
    return redirect('Login') 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if 'authdetails' in request.session:
        print("Session Auth")
        return render(request, 'index.html')
    return redirect('Login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def auth_view(request):
    if request.method == "POST":
        un = request.POST.get('username')
        up = request.POST.get('password')
        
        user = authenticate(request, username=un, password=up)
        if user:
            login(request, user)
            request.session['authdetails'] = un 
            return redirect('Index') 
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'auth.html', {'messages': messages.get_messages(request)})
    return render(request, 'auth.html')  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkSpam(request):
    if request.method == "POST":
        if 'authdetails' in request.session:
            algo = request.POST.get("algo")
            rawData = request.POST.get("rawdata")

            if algo == "Algo-1":
                return render(request, 'output.html', {"answer": model1.predict([rawData])[0]})
            elif algo == "Algo-2":
                return render(request, 'output.html', {"answer": model2.predict([rawData])[0]})
        else:
            return redirect('Login')  
    return redirect('Index')  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if 'authdetails' in request.session:
        logout(request)
        request.session.clear()  
        print("-----------------")
    return redirect('Login')  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "User created successfully")
            return redirect('Login') 
    return render(request, 'signup.html', {'messages': messages.get_messages(request)})