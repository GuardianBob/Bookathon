from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
# from loginApp.models import User

RATING_CHOICES = (
    ('1', 1), 
    ('2', 2), 
    ('3', 3), 
    ('4', 4), 
    ('5', 5)
    )

# This validation may not be necessary.  This was used prior to discovering how to use forms.py
class CheckBook(models.Manager):   
    def validator(self, postData):
        errors = {}
        if 'author' in postData:
            if postData['author'] != '':
                fName = postData['author'].split(" ", 1)[0]
                lName = postData['author'].split(" ", 1)[1]
                author_obj = Author.objects.filter(first_name__contains=fName).filter(last_name__contains=lName)
                if len(author_obj) > 0:
                    errors['author'] = "Author already exists"
                elif len(fName) < 2 or len(fName) < 2:
                        errors['author'] = "Name must be at least 2 non-numeric characters."
            elif postData['authorSel'] == '':
                errors['author'] = "Please specify an Author."              
        book_obj = Book.objects.filter(title=postData['title'])
        if len(book_obj) > 0:
            errors['title'] = "Book already exists."    
        elif len(postData['title']) < 2:
            errors['title'] = "Title must be at least 2 characters."       
        if postData['review'] != '': 
            if len(postData['review']) <= 10:
                errors['review'] = "Review must be longer than 10 characters"
            if postData['rating'] == '-' or 'rating' not in postData:
                errors['rating'] = "Please rate this book."
        return errors

# This validation may not be necessary.  This was used prior to discovering how to use forms.py
class CheckReview(models.Manager):
    def validate_review(self, postData):
        errors = {}
        if 'review' in postData or postData['review'] != '': 
            if len(postData['review']) <= 10:
                errors['review'] = "Review must be longer than 10 characters"            
        else:
            errors['review'] = "Please enter a review."
        if postData['rating'] == "" or 'rating' not in postData:
                errors['rating'] = "Please rate this book."
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, related_name='books_uploaded', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_books", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CheckBook()

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name="authors", blank=True)
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='book_reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CheckReview()

class Genre(models.Model):
    name = models.TextField()
    books = models.ManyToManyField(Book, related_name="genres_book", blank=True)
    author = models.ManyToManyField(Author, related_name="genres_author", blank=True)
    user = models.ManyToManyField(Book, related_name="genres_user", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
