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
from django.conf import settings
from .search import get_books_data, parse_book_info

book_api = settings.BOOKS_API

# NOTE: This is the original logged-in validation I used:
def get_user_id(request):
    if not 'user_id' in request.session:
        return None   
    else:
        user_id = request.session['user_id']
        return user_id

# Authentication keeps returning AnonymousUser when user is signed in
# This updates it to fix the problem
def validate_user(request):
    if request.user.is_authenticated is False:  # Initially this always returns false. 
    # request.user needs to be set here initially for some reason.  Once it is set, request.user 
    # will always be the logged in user and this will return True.
        user_id = get_user_id(request)
        # print(user_id)
        if not user_id is None:
            request.user = User.objects.get(id=user_id) # set request.user to logged in user
            return True
        else:
            return False
    else:
        return True

# called as the index/home page
def books(request):
    if validate_user(request) is False:  # Used to validate the user is logged in and set some request variables
        return redirect('/login') 
    # print('books_user: ', request.user)
    reviews = Review.objects.order_by('-created_at')[:3] # gets the 3 most recent reviews
    context = {
        'reviews': reviews,
        "user": request.user,
        'books': Book.objects.order_by('title')
    }
    return render(request, 'books.html', context)  

# called when someone is adding a book
def add(request):  
    if validate_user(request) is False:
        return redirect('/login')
    context = {
        "form": BookForm(), # BookForm is imported from forms.py
        "books": Book.objects.all(),
        "authors": Author.objects.all(),
        "user": request.user,
        "rateScale": range(1, 6),  
    }
    return render(request, "add.html", context)

# called when someone clicks on a book title
def book_info(request, book_id, form=ReviewForm()): 
    if validate_user(request) is False:
        return redirect('/login')    
    book = Book.objects.get(id=book_id)
    author = Author.objects.get(books__id=book_id)
    reviews = Review.objects.filter(book=book)
    new_form = form
    context = {
        "form": new_form,
        "book": book,
        "reviews": reviews,
        "author": author,
        "user": request.user,
    } 
    # print(context['form'])
    return render(request, "info.html", context)

# called when someone clicks on a username
def user_info(request, profile_id): 
    if validate_user(request) is False:
        return redirect('/login')
    profile = User.objects.get(id=profile_id)
    reviews = Review.objects.filter(user=profile)
    context = {
        'user': profile,
        'reviews': reviews,
    }
    return render(request, "user.html", context)

# called when someone posts a review for a book already in database
def update(request, book_id):
    if validate_user(request) is False:
        return redirect('/login')
    if not request.method == "POST":
        return redirect('/')
    form = ReviewForm(request.POST)
    if not form.is_valid():
        print('failed')    
        return book_info(request, book_id, form) 
    # NOTE This passes the form data back to the info page and eliminates about 8-10 lines of code.
    # NOTE NOTE  This only works if "books" is removed from the update url otherwise it doubles "update" in the url
    else:
        book = Book.objects.get(id=book_id)
        review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book=book, user=request.user)
    return redirect(f'/books/{book_id}')

# This was a workaround to clear form errors.  I don't believe it is necessary anymore
def clear(request, page, book_id=None):
    if 'errors' in request.session:
        del request.session['errors']
    if page == 'info':
        return redirect(f'/books/{book_id}')
    if page == 'new' or page == 'books':
        return redirect('/books')
    if page == 'add':
        return redirect('/books/add')
    if page == 'users':
        return redirect(f'/users/{book_id}')

# called when someone is adding a new book
def newBook(request):
    if not request.method == "POST":
        return redirect('/')
    if validate_user(request) is False:
        return redirect('/login')
    form = BookForm(request.POST)
    if not form.is_valid():
        context = { 'form': form, }
        return render(request, 'add.html', context)    
    # print(request.POST)     
    if not 'author_sel' in request.POST or request.POST['author_sel'] == '':        
        author_obj = checkAuthor(request.POST['author'])
    else:
        # print("author = " + request.POST['author_sel'])
        author_obj = Author.objects.get(id=request.POST['author_sel'])
    new_book = Book.objects.create(title=request.POST['title'], uploaded_by=request.user)
    author_obj.books.add(new_book)
    if request.POST['review'] != '':
        new_review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book=new_book, user=request.user)  
    return redirect(f'/books/{new_book.id}')

# called when a user wants to delete their own review
def del_review(request, review_id):
    if validate_user(request) is False:
        return redirect('/login')
    review = Review.objects.get(id=review_id)
    book_id = review.book.id
    if request.user.id == review.user.id:
        review.delete()
    return redirect(f'/books/{book_id}')
    
# used to verify that an author is not already in teh database before adding a book.
def checkAuthor(authName):
    fName = authName.split(" ", 1)[0]
    lName = authName.split(" ", 1)[1]
    author_obj = Author.objects.filter(first_name__contains=fName).filter(last_name__contains=lName)
    # print(len(author_obj))
    if len(author_obj) > 0:
        return author_obj
    else:
        new_author = Author.objects.create(first_name=fName, last_name=lName)
        return new_author

# ****************************************************************************
def test(request):   
    return render(request, 'test.html')

# COMMENTING OUT FOR NOW..... SO IT DOESN'T CLUSH WITH THE ONE BELOW. WILL TURN IT BACK ON ONCE THE BOOTTON IS DELETED
# def search(request):   
#     return render(request, 'search.html')

def book_query(request):
    query = request.POST['search'] #request.GET.get('q')
    books = get_books_data(query)
    context = {
        'books': books
    }

    return render(request, 'results.html', context)


def get_book_info(request, id):
    print(id)
    url = "https://books.googleapis.com/books/v1/volumes/" + id
    book_info = parse_book_info(url)
    print(book_info)
    context = {
        'book' : book_info
    }
    return None

def search(request):  
    context = {
        "book_api": book_api,
    }
    return render(request, 'search.html', context)

