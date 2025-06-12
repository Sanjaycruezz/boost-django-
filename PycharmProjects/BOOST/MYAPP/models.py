from django.db import models

# Create your models here.
class login_table(models.Model):
    user_name=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class user_table(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone_no=models.BigIntegerField()
    age=models.BigIntegerField()
    height=models.FloatField()
    weight=models.FloatField()
    photo = models.FileField()
    gender = models.CharField(max_length=100)

class doubt_table(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    doubts=models.CharField(max_length=100)
    reply=models.CharField(max_length=100)
    date=models.DateField()

class tips_table(models.Model):
    tips=models.CharField(max_length=100)
    details=models.CharField(max_length=100)
    date=models.DateField()

class complaint_table(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    complaint =models.CharField(max_length=100)
    reply = models.CharField(max_length=100,default='pending')
    date = models.DateField()

class feedback(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=500)
    date = models.DateField()

class chat_bot(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    answer = models.TextField(max_length=100)
    date = models.DateField()



class dietplan(models.Model):
    age = models.CharField(max_length=3)  # Age as string (e.g., 25)
    height = models.CharField(max_length=10)  # Height in cm
    weight = models.CharField(max_length=10)  # Weight in kg

    # Health and lifestyle fields
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    activity_level = models.CharField(max_length=10, choices=[('Sedentary', 'Sedentary'), ('Moderate', 'Moderate'), ('Active', 'Active')])
    goal = models.CharField(max_length=15, choices=[('Weight Loss', 'Weight Loss'), ('Weight Gain', 'Weight Gain'), ('Maintain', 'Maintain')])
    diet_type = models.CharField(max_length=10, choices=[('Veg', 'Veg'), ('Non-Veg', 'Non-Veg'), ('Vegan', 'Vegan')])
    medical_condition = models.CharField(max_length=100, choices=[('None', 'None'), ('Diabetes', 'Diabetes'), ('High BP', 'High BP')])




class workoutplan(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    goal=models.CharField(max_length=100)
    workoutdays=models.CharField(max_length=100)
    equipements=models.CharField(max_length=100)
    plank=models.BigIntegerField()
    squats=models.BigIntegerField()
    maximumpushup=models.BigIntegerField()

class Excercise(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    date = models.DateField()
    excercise = models.CharField(max_length=100)
    Count = models.BigIntegerField()


from django.contrib.auth.models import User
from django.db import models


class calorie(models.Model):
    date = models.DateField()
    cal_burn = models.BigIntegerField()