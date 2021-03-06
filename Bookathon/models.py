from django.db import models, connection
from django.contrib.auth.models import User, AbstractUser
# from loginApp.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

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
    google_id = models.TextField(max_length=255, unique=True) 
    desc = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, related_name='books_uploaded', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="favorite_books", blank=True)
    collection = models.ManyToManyField(User, related_name="collected_books", blank=True, default=0)
    rating = models.IntegerField(blank=True, null=True)
    image_link = models.CharField(max_length=255, blank=True, null=True)
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


# ====================================================== Following ======================================================

class Followers(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

# ====================================================== Profile ========================================================

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed

    # Override the save method of the model
    def save(self):
        super().save()

        img = Image.open(self.image.path) # Open image
        
        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) # Save it again and override the larger image