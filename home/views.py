from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Contact

from django.contrib.auth.models import User

from django.contrib.auth import login, logout, authenticate

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phoneNumber = request.POST['phone']
        content = request.POST['content']

        if len(name) > 4 or len(phoneNumber) > 11 or len(email) > 8 or len(content) > 20:
            contact = Contact(name=name, 
            email=email,
            phoneNumber=phoneNumber,  content=content)
            contact.save()
            messages.success(request, 'Your Form has been submitted successfully:')

        else:
            messages.error(request, "Your Form is not filled and can't submitted successfully:")

    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstName = request.POST['fname']
        secondName = request.POST['lname']
        email_id = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']

        if len(username) > 10:
            messages.error(request, 'Your username must be less then 10 alphabets:')
            return redirect('/')
        
        if password1 != password2:
            messages.error(request, 'Your Passwords do not Match, Try again:')
            return redirect('/')
        
        myUser = User.objects.create_user(username, email_id, password1)
        myUser.first_name = firstName
        myUser.last_name = secondName
        myUser.save()
        messages.success(request, 'Your Account has been created:')
        return redirect('/')
    else:
        return render(request, 'home/404-notfound.html')
    

def logIn(request):
    if request.method == 'POST':
        loginName = request.POST['loginusername']
        loginPasswrod = request.POST['loginpassword']

        userLogin = authenticate(username=loginName, password=loginPasswrod)
    
        if userLogin is not None:
            login(request, userLogin)
            messages.success(request, 'You have been successfully Logged In:')
            return redirect('/')
    
        else:
            messages.error(request, 'You can\'t Logged In, Try Again:')
            return redirect('/')
    else:
        return render(request, 'home/404-notfound.html')
    
def logOut(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully:')
    return redirect('/')