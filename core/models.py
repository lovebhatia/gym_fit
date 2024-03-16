from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    bio = models.CharField(max_length = 255, blank = True)
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)
    
    def __str__(self):
        return self.username
    
    
class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    title = models.CharField(max_length=100, null=True, blank=True)
    cover_image = models.ImageField(upload_to='images/', null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    
class ExerciseDay(models.Model):
    name_of_day = models.CharField(max_length = 100)
    created = models.DateTimeField(auto_now_add = True)
    
class Workout(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.username}'s workout on {self.date}"

class Exercise(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name
    
class Set(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.IntegerField()
    weight = models.FloatField()
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return f"{self.exercise.name}: {self.reps} reps, {self.weight} kg on {self.date}"
    
class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} did {self.activity} on {self.date}"
    
  
class ExerciseDataList(models.Model):
    name_of_parts_exercise = models.ForeignKey(ExerciseDay, on_delete = models.CASCADE, blank = True, related_name = 'exercise_list')
    name_of_exercise = models.CharField(max_length = 40, null = True)
    created = models.DateTimeField(auto_now_add = True)
    sets = models.CharField( max_length=50)
    gif = models.CharField(max_length = 500)
    description = models.CharField(max_length=500)
    
class Reps(models.Model):
    name_of_exercise = models.CharField(max_length = 40)
    created = models.DateTimeField(auto_now_add = True)
    sets = models.CharField(max_length = 20)

# This is the string representation of the object
    def __str__(self):
        return self.title
    
class BMIRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add = True)
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    height = models.FloatField(help_text="Height in meters")
    weight = models.FloatField(help_text="Weight in kilograms")
    age = models.PositiveIntegerField()
    bmi = models.FloatField(help_text="Body Mass Index")

    def __str__(self):
        return f"BMI Record for {self.user.username} on {self.date}"
    

        

