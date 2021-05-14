from django import forms
from .models import Book, Student, Review
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class StudentUser(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')        

class Student(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('batch', 'profile_pic')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'description')        