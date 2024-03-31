from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    username = models.CharField(max_length=100, unique=True)
    designation = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)


    def __str__(self):
        return self.username + " - " + self.designation
    



class Category(models.Model):
    name = models.CharField(max_length=50)


# blog model
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blogPost')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    summary = models.TextField(max_length=500)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " -> " + self.category



# dreaf model
class Draft(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blogPost')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    summary = models.TextField(max_length=500)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " -> " + self.category


class Appointment(models.Model):
    doctor_name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()