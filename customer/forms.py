from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# forms.py
from django import forms
from store.models import Review



class RegistrationForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))



    class Meta:
        model=User
        fields=["first_name","last_name","email","username"]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            
        }
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TimeInput(attrs={"class":"form-control"})) 
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))     




class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}), label="Shipping Address")



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5, 'class': 'form-control'}),
        }
