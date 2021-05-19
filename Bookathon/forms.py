from .models import Book, Author, Review
from loginApp.models import User
from django import forms
import datetime
from django.forms.widgets import TextInput

RATING_CHOICES = (
    ("", ""),
    ('1', 1), 
    ('2', 2), 
    ('3', 3), 
    ('4', 4), 
    ('5', 5)
    )

# Get author list dynamically each time:
def get_authors():
    authors = Author.objects.all().values_list('id', 'full_name')
    author_list = (("", ""),)
    for author in authors:
        author_list.append((f'{author[0]}', f'{author[1]}',))
    return author_list

class Date_In(TextInput):
    input_type = 'date'

class BookForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput)  
    author = forms.CharField(max_length=200, widget=forms.TextInput, required=False)
    # Dropdown field
    author_sel = forms.ChoiceField(widget=forms.Select, choices=get_authors, required=False) 
    review = forms.CharField(widget=forms.Textarea, required=False)
    rating = forms.ChoiceField(widget=forms.Select, choices=RATING_CHOICES, required=False)

    # Customize input forms:
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        # add a "form-control" class to each form input
        # for enabling bootstrap   
        # this automatically adds the class to the input forms each time they are called.   
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })        
        # Update the label of the selection
        self.fields['author_sel'].label = "Choose an author from the list:"           
        self.fields['review'].widget.attrs.update({ 'rows': '4' })
        self.fields['rating'].widget.attrs.update({ 'class': 'form-control w-25' })
                
    # Customize form input validation:
    def clean(self):
        super(BookForm, self).clean()
        title = self.cleaned_data.get('title')
        desc = self.cleaned_data.get('desc')
        author = self.cleaned_data.get('author')
        author_sel = self.cleaned_data.get('author_sel')
        review = self.cleaned_data.get('review')
        rating = self.cleaned_data.get('rating')
        
        # Validate Author Name
        if author_sel == '':
            if len(author) > 2 and author != '' and author_sel == '':                           
                fName = author.split(" ", 1)[0]
                lName = author.split(" ", 1)[1]
                author_obj = Author.objects.filter(first_name__contains=fName).filter(last_name__contains=lName)
                if len(author_obj) > 0:
                    self.errors['author'] = self.error_class([
                        'Author already exists'])
                elif len(fName) < 2 or len(fName) < 2:
                    self.errors['author'] = self.error_class([
                        'Name must be at least 2 non-numeric characters.'])
            else:
                self.errors['author'] = self.error_class([
                    'Please specify an Author.'])

        # Validate Book does not exist:
        book_obj = Book.objects.filter(title=title)
        if len(book_obj) > 0:
            self.errors['author'] = self.error_class([
                'Book already exists.'])   
        elif len(title) < 2: 
            self.errors['title'] = self.error_class([
                'Title must be at least 2 characters.'])     
        
        # Validate review entry:
        if review != '': 
            if len(review) <= 10:
                self.errors['review'] = self.error_class([
                    'Review must be longer than 10 characters.'])
            if rating == '-' or not len(rating) > 0 :
                self.errors['rating'] = self.error_class([
                    'Please rate this book.'])
        return self.cleaned_data

class ReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea)
    rating = forms.ChoiceField(widget=forms.Select, choices=RATING_CHOICES)    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
        self.fields['review'].widget.attrs.update({ 'rows': '4' })
        self.fields['rating'].widget.attrs.update({ 'class': 'form-control w-25' })

    def clean(self):
        super(ReviewForm, self).clean()            
        review = self.cleaned_data.get('review') 
        rating = self.cleaned_data.get('rating')       
        if len(review) <= 10:
            self.errors['review'] = self.error_class([
                'Review must be longer than 10 characters.'])
        if rating == '-' or not len(rating) > 0 :
            self.errors['rating'] = self.error_class([
                'Please rate this book.'])
        return self.cleaned_data
