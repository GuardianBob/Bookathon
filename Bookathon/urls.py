from django.urls import path        # These are the standard imports
from . import views, login

# NOTE: "name" argument at the end of path allows for dynamic url generation in the templates
# ex: In the template use "{% url 'add_book' %}".  This will generate a url to the correct path even if the
# path is changed here.  You can change 'books/add' to anything and django will pull the url path into the templates 
# without having to update the path in each html page. 

urlpatterns = [
    path('books', views.books, name="home"),
    path('books/add', views.add, name="add_book_page"),
    path('books/new_book', views.newBook, name="submit_new_book"),
    path('update/<int:bid>', views.update, name="submit_review"),
    path('books/<int:bid>', views.book_info, name="book_info"),
    path('users/<int:uid>', views.user_info, name="user_profile"),
    path('books/delete/<int:rid>', views.del_review, name="delete_review"),
    path('cl/<str:page>/<int:bid>', views.clear, name="clear_errors"),
]