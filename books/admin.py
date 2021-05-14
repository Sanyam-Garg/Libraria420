from django.contrib import admin
from .models import Book, Student, IssuedBooks, Review
# Register your models here.
admin.site.register(Book)
admin.site.register(Student)
admin.site.register(IssuedBooks)
admin.site.register(Review)
