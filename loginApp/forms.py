from .models import User
from django import forms
import datetime
import bcrypt

LEVEL_SELECT = (
    ('False', 'Normal'),
    ('True', 'Admin')
)

USER_TYPE_SELECT = (
    ('', ''),
    ('doctor', 'Doctor'),
    ('intern', 'Intern'),
    ('technician', 'Technician'),
    ('staff', 'Staff'),
    ('supervisor', 'Supervisor')
)

STATE_SELECT = (
    ('', ''),
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AS', 'American Samoa'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('GU', 'Guam'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('MP', 'Northern Mariana Islands'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('PR', 'Puerto Rico'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VI', 'Virgin Islands'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming')
)

class Register_Form(forms.Form):
    first_name = forms.CharField(max_length=200, widget=forms.TextInput, required=True)
    last_name = forms.CharField(max_length=200, widget=forms.TextInput, required=True)  
    email = forms.EmailField(max_length=200, widget=forms.EmailInput, required=True)
    address = forms.CharField(max_length=150, widget=forms.TextInput, required=False)
    address_line2 = forms.CharField(max_length=150, widget=forms.TextInput, required=False)
    apt_num = forms.CharField(max_length=10, widget=forms.TextInput, required=False)
    city = forms.CharField(max_length=35, widget=forms.TextInput, required=False)
    state = forms.ChoiceField(widget=forms.Select, choices=STATE_SELECT, required=False)
    zipcode = forms.IntegerField(widget=forms.TextInput, required=False)
    password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=True)
    check_pass = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super(Register_Form, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })
        self.fields['password'].widget.attrs.update({
            'id': 'password',
        })
        self.fields['check_pass'].widget.attrs.update({
            'class' : 'form-control',
            'id': 'check_pass',
            'onChange': 'checkPass();'
        })
        self.fields['password'].label = 'Password'
        self.fields['check_pass'].label = 'Password Confirmation'

    def clean(self):
        super(Register_Form, self).clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        address = self.cleaned_data.get('address')
        address_line2 = self.cleaned_data.get('address_line2')
        apt_num = self.cleaned_data.get('apt_num')
        city = self.cleaned_data.get('city')
        state = self.cleaned_data.get('state')
        zipcode = self.cleaned_data.get('zipcode')
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
    # user_id = forms.CharField(max_length=200, widget=forms.TextInput)
    first_name = forms.CharField(max_length=200, widget=forms.TextInput)
    last_name = forms.CharField(max_length=200, widget=forms.TextInput)  
    email = forms.EmailField(max_length=200, widget=forms.EmailInput)
    user_level = forms.ChoiceField(widget=forms.Select, choices=LEVEL_SELECT, required=False)
    user_type = forms.ChoiceField(widget=forms.Select, choices=USER_TYPE_SELECT, required=False)
    address = forms.CharField(max_length=150, widget=forms.TextInput, required=False)
    address_line2 = forms.CharField(max_length=150, widget=forms.TextInput, required=False)
    apt_num = forms.CharField(max_length=10, widget=forms.TextInput, required=False)
    city = forms.CharField(max_length=35, widget=forms.TextInput, required=False)
    state = forms.ChoiceField(widget=forms.Select, choices=STATE_SELECT, required=False)
    zipcode = forms.IntegerField(widget=forms.TextInput, required=False)
    # password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=False)
    # check_pass = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput, required=False)

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
        user_level = self.cleaned_data.get('user_level')
        user_type = self.cleaned_data.get('user_type')
        address = self.cleaned_data.get('address')
        address_line2 = self.cleaned_data.get('address_line2')
        apt_num = self.cleaned_data.get('apt_num')
        city = self.cleaned_data.get('city')
        state = self.cleaned_data.get('state')
        zipcode = self.cleaned_data.get('zipcode')
                
        # def check_string(string, length, varName):
        #     if len(string) < length: 
        #         self.errors[f"{varName}"] = self.error_class([
        #             f'Input must be at least 2 characters.'])
        #         print('error failed')

        # check_string(first_name, 2, 'first_name')
        # check_string(last_name, 3, 'last_name')
                
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
        self.fields['password'].label = 'Password'
        self.fields['check_password'].label = 'Password Confirmation'

    def clean(self):
        super(UpdatePasswordForm, self).clean()
        password = self.cleaned_data.get('password')
        user_id = self.cleaned_data.get('user_id')
                
        user = User.objects.get(id=user_id)       

        
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            self.errors['password'] = self.error_class([
                f'Password cannot be the same as previous password.'])

        return self.cleaned_data