from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User as User_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

from .models import Profiling

def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password_one = request.POST['password']
        password_two = request.POST['cPassword']

        if User_login.objects.filter(username=username).exists():
            messages.error(request, 'User already Exists')
        
        elif (username and email and password_one and password_two):
            
            # Creating The User Object.
            auth_user = User_login.objects.create_user(username=username, email=email, password=password_one)
            
            #Getting the created User Object saved to the custom Database.
            Profiling.objects.create(user=auth_user, username=username, password=password_one, email=email)

            auth_user.password_one = password_one
            auth_user.password_two = password_two
            auth_user.save()
            messages.success(request, 'Your Account has been created Successfully:')
            return redirect('/login')
    return render(request, 'home/sign-up.html')


def loginAccount(request):
    if request.method == 'POST':
        username = request.POST['username']
        login_password = request.POST['password']


        if not Profiling.objects.filter(username=username).exists():
            User_login.objects.filter(username=username, is_superuser=False).delete()
            request.session.flush() #* Getting the complete session flushed and reload it to avoid the csrf token verification being failed
            
            return redirect('signup')
        
        # Verifying The credientials and returning the Object of the User. If the requested User is Valid.
        user = authenticate(username=username, password=login_password)

        if user is None:
            messages.error(request, 'Failed Login Attempt, Try Again Please!')
            return redirect('login')

        else:
            auth_login(request, user)
            messages.success(request, 'Login Successfully Completed:')
            return redirect('/')
        
    return render(request, 'home/login.html')

def handle_logout(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out:')
    return redirect('/')

def user(request):
    # Data getting fetched:
    user = Profiling.objects.get(user=request.user)
    context = {
        'users': user
    }
    return render(request, 'home/user_profile_page.html', context)