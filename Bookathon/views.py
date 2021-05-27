from django.shortcuts import render, redirect
from .models import Book, Author, Review, Followers
# from loginApp.models import User, Address
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core import serializers
from .forms import BookForm, ReviewForm, ProfileUpdateForm 
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
def book_info(request, google_id, form=ReviewForm()): 
    if validate_user(request) is False:
        return redirect('/login')        
    book_info = get_book_info(google_id)      
    collected = False
    if len(Book.objects.filter(google_id=google_id).filter(collection=request.user)) > 0:
        collected = True
    # print(collected)
    context = {
        "form": form,
        'book_info': book_info,
        "user": request.user,
        "author": book_info['authors'][0],
        "in_collection": collected, 
    } 
    if len(Book.objects.filter(google_id=google_id)) > 0:
        book = Book.objects.get(google_id=google_id)
        reviews = Review.objects.filter(book=book)
        book = Book.objects.get(google_id=google_id)
        author = Author.objects.get(books__id=book.id)
        context.update({
            "reviews": reviews, 
        })
    # print(context['form'])
    return render(request, "info.html", context)

# called when someone clicks on a username
def user_info(request, profile_id): 
    if validate_user(request) is False:
        return redirect('/login')
    profile = User.objects.get(id=profile_id)
    reviews = Review.objects.filter(user=profile)
    followers = {}
    for user in profile.followers.all():
        follower = User.objects.get(id=user.user_id)
        followers.update( {follower.id : follower.username } )
    following = {}
    for user in profile.following.all():
        follows = User.objects.get(id=user.following_user_id)
        following.update( {follows.id : follows.username } )
    is_followed = False
    # print(followers, request.user.id)
    if request.user.id in followers.keys():
        is_followed=True
    else:
        is_followed=False

    context = {
        'user': request.user,
        'reviews': reviews,
        'profile': profile,
        'followers': followers, 
        'following': following,
        'is_followed':is_followed
    }
    return render(request, "user.html", context)

def user_collection(request, profile_id): 
    if validate_user(request) is False:
        return redirect('/login')
    profile = User.objects.get(id=profile_id)
    books = Book.objects.filter(collection=profile)
    context = {
        'user': profile,
        'books': books,
    }
    return render(request, "user_books.html", context)

# called when someone posts a review for a book already in database
def update(request, google_id):
    if validate_user(request) is False:
        return redirect('/login')
    if not request.method == "POST":
        return redirect('/')
    form = ReviewForm(request.POST)
    if not form.is_valid():
        print('failed')    
        return book_info(request, google_id, form)
    # NOTE This passes the form data back to the info page and eliminates about 8-10 lines of code.
    # NOTE NOTE  This only works if "books" is removed from the update url otherwise it doubles "update" in the url
    else:
        book_info = get_book_info(google_id)
        book = check_book(request, book_info)
        review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book=book, user=request.user)
    return redirect(f'/info/{google_id}')

# This was a workaround to clear form errors.  I don't believe it is necessary anymore
def clear(request, page, book_id=None):
    if 'errors' in request.session:
        del request.session['errors']
    if page == 'info':
        return redirect(f'/info/{book_id}')
    if page == 'new' or page == 'books':
        return redirect('/')
    if page == 'add':
        return redirect('/add')
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
    return redirect(f'/info/{new_book.id}')

def add_book(request, book):
    if validate_user(request) is False:
        return redirect('/login')        
    collected_book = check_book(request, book)
    collected_book.collection.add(request.user)
    return collected_book


# called when a user wants to delete their own review
def del_review(request, review_id):
    if validate_user(request) is False:
        return redirect('/login')
    review = Review.objects.get(id=review_id)
    book_id = review.book.id
    if request.user.id == review.user.id:
        review.delete()
    return redirect(f'/info/{book_id}')
    
# used to verify that an author is not already in teh database before adding a book.
def checkAuthor(authName):
    # Use .rsplit() to split starting from the end going backwards.
    fName = authName.split(" ", 1)[0]
    # tmp = authName.split(" ", 1)[1]
    # middle = tmp.rsplit(" ", 1)[0]
    lName = authName.rsplit(" ", 1)[1]
    author_obj = Author.objects.filter(first_name__contains=fName).filter(last_name__contains=lName)
    # print(len(author_obj))
    if len(author_obj) > 0:
        return author_obj[0]
    else:
        new_author = Author.objects.create(first_name=fName, last_name=lName)
        return new_author

# Check if book exists in database
def check_book(request, book):
    if not len(Book.objects.filter(google_id=book['id'])) > 0:
        collected_book = Book.objects.create(title=book['title'], google_id=book['id'], uploaded_by=request.user)
        author = checkAuthor(book['authors'][0])
        collected_book.authors.add(author)
    else:
        collected_book = Book.objects.get(google_id=book['id'])
    return collected_book

def remove_from_collection(request, book_id):
    if validate_user(request) is False:
        return redirect('/login')
    book = Book.objects.get(id=book_id)
    request.user.collected_books.remove(book)
    book_list = request.user.collected_books.all()
    books = []
    for book in book_list:
        books.append({
            'id': book.id,
            'title': book.title,
            'google_id': book.google_id,
        })
    response = {'books': books}
    print(books)
    return JsonResponse(response)
# ****************************************************************************
def book(request):   
    return render(request, 'book.html')  #testing this one!!!

# def test(request):   
#     return render(request, 'test.html')

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

def get_book_info(book_id):
    # print(book_id)
    url = f"https://books.googleapis.com/books/v1/volumes/{book_id}"
    book_info = parse_book_info(url)
    return book_info

def search(request): 
    if validate_user(request) is False:
        return redirect('/login')
    context = {
        "book_api": book_api,
        "user": request.user,
    }
    return render(request, 'search.html', context)

def add_from_search(request, book_id):
    # print(book_id)
    if validate_user(request) is False:
        return redirect('/login')
    book_info = get_book_info(book_id)
    add_book(request, book_info)
    
    return HttpResponse('Ok!')
  
# ====================================================== Following ======================================================

def follow_user(request, user_id):
    if validate_user(request) is False:
        return redirect('/login')
    user_to_follow = User.objects.get(id=user_id)
    current_user = User.objects.get(id=request.user.id)
    is_followed = False
    if user_to_follow != current_user:
        if current_user.following.filter(following_user_id=user_to_follow.id).exists():
            # print("check worked")
            current_user.following.filter(following_user_id=user_to_follow.id).delete()
            is_followed = False
        else:
            # print("check_failed")
            Followers.objects.create(user=current_user, following_user=user_to_follow)
            is_followed = True
        return redirect(f'/users/{user_id}')
    else:
        return redirect(f'/users/{user_id}')

# ***************************************** Testing ********************************************************************

def profile(request):
    context = {
        'profile_form': ProfileUpdateForm() # ProfileUpdateForm is imported from forms.py
    }
    return render(request, 'profile.html', context)


# ============= Profile Update here ================

def profile(request):
    if validate_user(request) is False:
        return redirect('/login')
    if request.method == 'POST':
        # u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile) 
        # if u_form.is_valid() and p_form.is_valid():
        #     u_form.save()
        #     p_form.save()
        #     messages.success(request, f'Your account has been updated!')
        #     return redirect('profile') # Redirect back to profile page

    else:
        # u_form = UpdateUserForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        # 'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)