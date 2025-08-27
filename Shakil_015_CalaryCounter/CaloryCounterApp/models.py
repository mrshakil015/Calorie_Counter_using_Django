from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class AuthUserModel(AbstractUser):
    
    def __str__(self):
        return self.username
    
class UserProfileModel(models.Model):
    GENDER_TYPES = [
        ('Male','Male'),
        ('Female','Female'),
    ]
    user = models.OneToOneField(AuthUserModel, on_delete=models.CASCADE, null=True, related_name='profile_user')
    Name = models.CharField(max_length=200, null=True)
    Age = models.PositiveIntegerField(null=True)
    Gender = models.CharField(choices=GENDER_TYPES, max_length=20, null=True)
    Height = models.FloatField(null=True, help_text='Height in cm')
    Weight = models.FloatField(null=True, help_text='Weight in kg')
    
    def __str__(self):
        return self.user.username


class DailyConsumedCalorieModel(models.Model):
    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, null=True, related_name='user_daily_consumed_calorie')
    Item_name = models.CharField(max_length=200, null=True)
    Calorie = models.FloatField(null=True)
    Date = models.DateField(null=True)
    
    def __str__(self):
        return f"{self.user.username}-{self.Item_name}-{self.Calorie}"
    
class TotalConsumedModel(models.Model):
    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, null=True, related_name='user_total_consumed')
    Total_calorie = models.FloatField(null=True)
    Date = models.DateField(null=True)
    
    def __str__(self):
        return f"{self.user.username}-{self.Total_calorie}-{self.Date}"