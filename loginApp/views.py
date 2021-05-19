from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import logout
import bcrypt
from .forms import Register_Form, Login_Form

def get_nav(request):
    nav = 'nav_out.html'
    if 'user_id' in request.session:
        nav = "nav_in.html"
    return nav

def welcome(request):
    start_btn = "/login/login"
    if 'user_id' in request.session:
        start_btn = "/dashboard"
    context = {
        'nav': get_nav(request),
        'start_btn': start_btn
    }
    return render(request, 'welcome.html', context)

def login(request, login_form=Login_Form()):
    context = {
        'login_form': login_form,
        'nav': get_nav(request),
        'page_title': 'Login Form',
        }
    return render(request, 'login.html', context)

def register(request, register_form=Register_Form()):    
    context = {
        'register_form' : register_form,
        'nav': get_nav(request),
        }
    return render(request, 'register.html', context)

def validate_register(request):    
    if request.method != "POST":
        return redirect("register")
    check_form = Register_Form(request.POST)    
    if not check_form.is_valid():
        login_form = Login_Form()
        context = { 
            'register_form': check_form,
            'nav': get_nav(request),
            }  
        page = 'login.html'
        if 'user_id' in request.session:
            page = 'add_user.html'      
        return render(request, page, context)
    else:
        passwd = request.POST['password']
        uPass = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt()).decode()
        level = False
        if len(User.objects.all()) == 0:
            level = True
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=uPass, user_level=level)
        return True

def add_new_user(request):
    validate_register(request)
    return redirect('/manage_users')
    
def new_registration(request):
    if validate_register(request) == True:
        if not 'user_id' in request.session:  
            user = User.objects.get(email=request.POST['email'])      
            request.session["user_id"] = user.id
    return redirect('/')

def validate_login(request):
    if request.method != "POST":
        return redirect("login")
    check_form = Login_Form(request.POST)
    if not check_form.is_valid():
        print('failed!')
        register_form = Register_Form()
        context = { 
            'login_form' : check_form,
            'nav': get_nav(request),
            }
        return render(request, 'login.html', context)
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session["user_id"] = user.id
        return redirect('/')

# def success(request):
#     if not 'name' in request.session: 
#         return redirect('')
#     context = {
#             'name': request.session['name'],
#             'login': request.session["login"]
#         }
#     return render(request, 'success.html', context)

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/')

