from django import forms
from .models import *

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = ['Name','Age', 'Gender', 'Height','Weight']
        
class DailyConsumedCalorieForm(forms.ModelForm):
    class Meta:
        model = DailyConsumedCalorieModel
        fields = ['Item_name','Calorie','Date']
        
        widgets = {
                'Date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }