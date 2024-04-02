from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from scrapboxapp.models import UserProfile,Scrap,Category,Bids

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user",)

class ScrapForm(forms.ModelForm):
    class Meta:
        model=Scrap
        exclude=("user",)

        widgets={
            "name":forms.TextInput(attrs={"class":"form-control","placeholder":"Product name: Eg: Samsung Gallaxy"}),
            "category":forms.Select(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control","placeholder":"Eg:₹ 24999"}),
            "description":forms.TextInput(attrs={"class":"form-control","placeholder":"Eg: 8GB Ram, 124GB Rom, AMOLED display"}),
            "location":forms.TextInput(attrs={"class":"form-control","placeholder":"Eg: Kakkanadu, Kochi, Kerala, India"}),
            "scrap_image":forms.FileInput(attrs={"class":"form-control"}),
            "condition":forms.TextInput(attrs={"class":"form-control","placeholder":"Eg: Working condition"}),
            "status":forms.Select(attrs={"class":"form-control"}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields="__all__"

class BidsForm(forms.ModelForm):
    class Meta:
        model= Bids
        fields=["amount"]
    
class ProductSearchForm(forms.Form):
    product=forms.CharField(max_length=30,required=False)
    description=forms.CharField(max_length=30,required=False)