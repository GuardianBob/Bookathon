from django.urls import path        # These are the standard imports
from . import views, login

# NOTE: "name" argument at the end of path allows for dynamic url generation in the templates
# ex: In the template use "{% url 'add_book' %}".  This will generate a url to the correct path even if the
# path is changed here.  You can change 'books/add' to anything and django will pull the url path into the templates 
# without having to update the path in each html page. 

urlpatterns = [
    path('books', views.books, name="home"),  # Link to the home page
    path('books/add', views.add, name="add_book_page"), # link to add a new book
    path('books/new_book', views.newBook, name="submit_new_book"), # called from the form after adding a new book to enter the info into the database
    path('update/<int:book_id>', views.update, name="submit_update"), # called from the review form on a book's info page to add the new review
    path('books/<int:book_id>', views.book_info, name="book_info"), # link to show a book's info
    path('users/<int:profile_id>', views.user_info, name="user_profile"), # link to show a user's profile
    path('books/delete/<int:review_id>', views.del_review, name="delete_review"), # called when a user clicks to remove their review
    path('cl/<str:page>/<int:book_id>', views.clear, name="clear_errors"), # old workaround that may no longer be necessary (depreciated)
    # **********************************************************************
    path('books/test', views.test, name="test"),
    path('books/search', views.search, name="search"),
    path('books/test_search', views.book_query, name="test_search"),
    path('books/json/<str:book_id>', views.get_book_info, name="fetch_book"),
    path('books/add/<str:book_id>', views.add_from_search, name="add_from_search"),
]