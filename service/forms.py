from django import forms



class UserRegisterationForm(forms.Form):
    email  = forms.EmailField(max_length=100, label="Email" )
    password = forms.CharField(widget=forms.PasswordInput(), label='password')
    
    
    