from django.shortcuts import render, redirect
# from .models import User
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
import bcrypt
from .forms import Register_Form, Login_Form, UpdateUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.decorators import login_required #NOT SURE ABOUT THIS, CHECK WITH JESSE!!!!

def index(request):
    # This is intended for a welcome splash page
    # Currently this redirects to the books homepage if a user is logged in or the login page if they are not
    return redirect('/')

def login(request, login_form=Login_Form()):
    context = {
        'login_form': AuthenticationForm(), #login_form,
        'page_title': 'Login Form',
        }
    return render(request, 'login.html', context)

def register(request, register_form=Register_Form()):    
    context = {
        'register_form' : register_form,
        }
    return render(request, 'register.html', context)

def validate_register(request):    
    if request.method != "POST":
        return redirect("register")
    check_form = Register_Form(request.POST)    
    if not check_form.is_valid():
        print('registration failed!')
        # print(check_form)
        login_form = Login_Form()
        context = { 
            'register_form': check_form,
            }  
        page = 'register.html'
        if 'user_id' in request.session:
            page = 'add_user.html'      
        return render(request, page, context)
    else:
        print('registration successful!')
        password = check_form.cleaned_data['password1']   
        # NOTE Django's User model uses it's own hash system for passwords on the backend so we don't need to implement bcrypt here
        user = User.objects.create_user(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=password, username=request.POST['username'])
        request.session['user_id'] = user.id
        request.user = user
        return redirect('/')
    
def validate_login(request):
    if request.method != "POST":
        return redirect("login")
    # check_form = Login_Form(request.POST)
    # print(request.POST)
    # NOTE: this is Django's backend authorization function.
    # currently it only works with usernames.
    user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
    # if not check_form.is_valid():
    # print(user)
    if user is None:
        print('failed!')
        register_form = Register_Form()
        context = { 
            'login_form' : AuthenticationForm(),
            }
        return render(request, 'login.html', context)
    else:
        # user = User.objects.get(email=request.POST['login_email'])
        request.session["user_id"] = user.id
        request.user = user
        return redirect('/')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/')

