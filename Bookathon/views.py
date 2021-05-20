from django.shortcuts import render, redirect
from .models import Book, Author, Review
# from loginApp.models import User, Address
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core import serializers
from .forms import BookForm, ReviewForm
from django.contrib import messages
import bcrypt
from django.utils import timezone
from datetime import datetime, date

# NOTE: This is the original logged-in validation I used:
def validate_user_logged_in(request):
    if not 'user_id' in request.session:
        return False   
    else:
        user_id = request.session['user_id']
        return user_id


def books(request):   
    user_id = validate_user_logged_in(request)
    if user_id is False: 
        return redirect('/login') 
    reviews = Review.objects.order_by('-created_at')[:3]
    context = {
        'reviews': reviews,
        "user": User.objects.get(id=user_id),
        'books': Book.objects.order_by('title')
    }
    return render(request, 'books.html', context)

def add(request):
    user_id = validate_user_logged_in(request)
    if user_id is False: 
        return redirect('/login') 
    new_form = BookForm()
    context = {
        "form": new_form,
        "books": Book.objects.all(),
        "authors": Author.objects.all(),
        "user": User.objects.get(id=user_id),
        "rateScale": range(1, 6),        
    }
    # if 'errors' in request.session:
    #     context['errors'] = request.session['errors']
    return render(request, "add.html", context)

def book_info(request, bid, form=ReviewForm()):    
    user_id = validate_user_logged_in(request)
    if user_id is False: 
        return redirect('/login') 
    user_id = request.session['user_id']
    book = Book.objects.get(id=bid)
    author = Author.objects.get(books__id=bid)
    reviews = Review.objects.filter(book=book)
    new_form = form
    context = {
        "form": new_form,
        "book": book,
        "reviews": reviews,
        "author": author,
        "user": User.objects.get(id=user_id),
    } 
    print(context['form'])
    return render(request, "info.html", context)

def user_info(request, uid):
    user = User.objects.get(id=uid)
    reviews = Review.objects.filter(user=user)
    context = {
        'user': user,
        'reviews': reviews,
    }
    return render(request, "user.html", context)

def update(request, bid):
    if not request.method == "POST":
        return redirect('/')
    form = ReviewForm(request.POST)
    if not form.is_valid():
        print('failed')    
        return book_info(request, bid, form) 
    # NOTE This passes the form data back to the info page and eliminates about 8-10 lines of code.
    # NOTE NOTE  This only works if "books" is removed from the update url otherwise it doubles "update" in the url
    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.get(id=bid)
        review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book=book, user=user)
    return redirect(f'/info/{bid}')

def clear(request, page, bid=None):
    if 'errors' in request.session:
        del request.session['errors']
    if page == 'info':
        return redirect(f'/books/{bid}')
    if page == 'new' or page == 'books':
        return redirect('/books')
    if page == 'add':
        return redirect('/books/add')
    if page == 'users':
        return redirect(f'/users/{bid}')

def newBook(request):
    if not request.method == "POST":
        return redirect('/')
    form = BookForm(request.POST)
    if not form.is_valid():
        context = { 'form': form, }
        return render(request, 'add.html', context)    
    print(request.POST)     
    if not 'author_sel' in request.POST or request.POST['author_sel'] == '':        
        author_obj = checkAuthor(request.POST['author'])
    else:
        # print("author = " + request.POST['author_sel'])
        author_obj = Author.objects.get(id=request.POST['author_sel'])
    user = User.objects.get(id=request.session['user_id'])
    new_book = Book.objects.create(title=request.POST['title'], uploaded_by=user)
    author_obj.books.add(new_book)
    if request.POST['review'] != '':
        new_review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book=new_book, user=user)  
    return redirect(f'/books/{new_book.id}')

def del_review(request, rid):
    review = Review.objects.get(id=rid)
    bid = review.book.id
    if request.session['user_id'] == review.user.id:
        review.delete()
    return redirect(f'/books/{bid}')
    
def checkAuthor(authName):
    fName = authName.split(" ", 1)[0]
    lName = authName.split(" ", 1)[1]
    author_obj = Author.objects.filter(first_name__contains=fName).filter(last_name__contains=lName)
    print(len(author_obj))
    if len(author_obj) > 0:
        return author_obj
    else:
        new_author = Author.objects.create(first_name=fName, last_name=lName)
        return new_author


