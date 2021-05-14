from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    published_by = models.CharField(max_length=50)
    cover = models.ImageField(upload_to = 'covers', blank = True, null = True)

    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.OneToOneField(User, related_name = 'student_user', on_delete = models.CASCADE)
    profile_pic = models.ImageField(upload_to = 'profile_pics', blank = True, null = True)

    batches = (
        (2020, '2020'),
        (2019, '2019'),
        (2018, '2018'),
        (2017, '2017'),
        (2016, '2016')
    )
    batch = models.IntegerField(choices = batches)

    def __str__(self):
        return self.user.username
    
class IssuedBooks(models.Model):
    student = models.ForeignKey(User, on_delete = models.CASCADE, related_name='student_issue')
    book = models.ForeignKey(Book, on_delete = models.CASCADE)
    issue_period = models.DateTimeField(auto_now_add = False, blank = True, null=True)

    def __str__(self):
        return self.student.username

class Review(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)

    def __str__(self):
        return self.title
            
        