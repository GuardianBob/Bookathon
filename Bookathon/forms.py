from .models import Book, Author, Review, Profile
# from loginApp.models import User
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import datetime, bcrypt
from django.forms.widgets import TextInput


RATING_CHOICES = (
    ("", ""),
    ('1', 1), 
    ('2', 2), 
    ('3', 3), 
    ('4', 4), 
    ('5', 5)
    )

COLLECTION_STATUS = (
    (0 , 'Plan To Read'),
    (1 , 'Reading'),
    (2, 'Already Read'),
    (3, 'Stopped Reading'),
    (4, 'On-Hold')
    )

# Get author list dynamically each time:
def get_authors():
    authors = Author.objects.all().values_list('id', 'first_name', 'last_name')
    author_list = [("", ""),]
    for author in authors:
        author_list.append((f'{author[0]}', f'{author[1]} {author[2]}',))
    return author_list

class Date_In(TextInput):
    input_type = 'date'

class BookForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput)
    # Dropdown field
    author_sel = forms.ChoiceField(widget=forms.Select, choices=get_authors, required=False)  #choices calls a query each time it is created.
    author = forms.CharField(max_length=200, widget=forms.TextInput, required=False)
    collected = forms.ChoiceField(widget=forms.Select, choices=COLLECTION_STATUS, required=False) 
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
        self.fields['author'].label = "Or add author here:"  
        self.fields['collected'].label = "Current Status:"  
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

class Register_Form(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput, required=True)
    last_name = forms.CharField(max_length=50, widget=forms.TextInput, required=True)  
    email = forms.EmailField(max_length=50, widget=forms.EmailInput, required=True)
    # password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=True)
    # check_pass = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(Register_Form, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })
        self.fields['password1'].widget.attrs.update({
            'id': 'password1',
        })
        self.fields['password2'].widget.attrs.update({
            'class' : 'form-control',
            'id': 'password2',
            'onChange': 'checkPass();'
        })
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Password Confirmation'

    def clean(self):
        super(Register_Form, self).clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        # password = self.cleaned_data.get('password')
        # check_pass = self.cleaned_data.get('check_pass')
        
        def check_string(string, length, varName):
            if len(string) < length: 
                self.errors[f"{varName}"] = self.error_class([
                    f'Input must be at least 2 characters.'])

        check_string(first_name, 2, 'first_name')
        check_string(last_name, 3, 'last_name')

        if len(User.objects.filter(email=email)) > 0: 
                self.errors[f"email"] = self.error_class([
                    f'This email already exists in the system'])
        return self.cleaned_data

class Login_Form(forms.Form): 
    login_email = forms.EmailField(max_length=200, widget=forms.EmailInput)
    login_password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(Login_Form, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })
            self.fields['login_password'].widget.attrs.update({
                'class' : 'form-control',
                'id' : 'login_password',
                'onChange': 'passEnbl();'
            })
            self.fields['login_password'].label = 'Password'

    def clean(self):
        super(Login_Form, self).clean()
        email = self.cleaned_data.get('login_email')
        password = self.cleaned_data.get('login_password')

        if not len(User.objects.filter(email=email)) > 0:
            self.errors[f'login_email'] = self.error_class([
                    f'Email or password is invalid'])
        else:
            stored_data = User.objects.get(email=email)
            if not bcrypt.checkpw(password.encode(), stored_data.password.encode()):
                self.errors[f'login_email'] = self.error_class([
                    f'Email or password is invalid'])
        return self.cleaned_data

class UpdateUserForm(forms.Form):
    first_name = forms.CharField(max_length=200, widget=forms.TextInput)
    last_name = forms.CharField(max_length=200, widget=forms.TextInput)  
    email = forms.EmailField(max_length=200, widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })
            # self.fields['description'].widget.attrs.update({
            #     'class' : 'form-control',
            #     'id': 'des',
            # })        
            self.initial['state'] = 'CA'
        
    def clean(self):
        super(UpdateUserForm, self).clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
                
                
        return self.cleaned_data

class UpdatePasswordForm(forms.Form):
    user_id = forms.CharField(max_length=200, widget=forms.TextInput)
    password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=False)
    check_password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })
        self.fields['password'].widget.attrs.update({
            'id': 'password',
        })
        self.fields['check_password'].widget.attrs.update({
            'class' : 'form-control',
            'id': 'check_password',
            'onChange': 'checkPass();'
        })
        self.fields['user_id'].widget.attrs.update({
            'class' : 'form-control',
            'id': 'user_id',
        })
        self.fields['password'].l

# ========= ProfileUpdateForm to update image ==========================
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']