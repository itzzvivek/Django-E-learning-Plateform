from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from core.email_backend import EmailBackEnd

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        #check mail
        if User.objects.filter(email=email).exists():
            messages.warning(request,'Email are Already Exists !')
            return redirect('register')
        
        #check usernane
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username are Already Exists !')
            return redirect('register')
        
        user = User(
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request,'registration/register.html')


def login(request):
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = EmailBackEnd.authenticate(request,
                                    username = email,
                                    password = password)
        if user != None:
            login(request.user)
            return redirect('home')
        else:
            messages.error(request,'Email and password are invalid !')
            return redirect('login')
    