from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import datetime
import bcrypt

LEVEL_SELECT = (
    ('False', 'Normal'),
    ('True', 'Admin')
)

class Register_Form(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput, required=False)
    last_name = forms.CharField(max_length=50, widget=forms.TextInput, required=False)  
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
        # self.fields['password'].widget.attrs.update({
        #     'id': 'password',
        # })
        # self.fields['check_pass'].widget.attrs.update({
        #     'class' : 'form-control',
        #     'id': 'check_pass',
        #     'onChange': 'checkPass();'
        # })
        # self.fields['password'].label = 'Password'
        # self.fields['check_pass'].label = 'Password Confirmation'

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

        # check_string(first_name, 2, 'first_name')
        # check_string(last_name, 3, 'last_name')

        if len(User.objects.filter(email=email)) > 0: 
                self.errors[f"email"] = self.error_class([
                    f'This email already exists in the system'])
        return self.cleaned_data

class Login_Form(forms.Form): 
    login_email = forms.EmailField(max_length=200, widget=forms.EmailInput)
    login_password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'password1']

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