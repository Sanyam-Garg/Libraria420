from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Book, Genre, Review, Student, IssuedBooks
from . import forms
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

import datetime

# Create your views here.
def index(request):
    books = Book.objects.order_by('title').all()

    diction = {
        'books': books,
    }
    return render(request, 'books/index.html', context = diction)

def add_book(request):

    if request.user.is_staff:

        if request.method == 'POST':
            form = forms.BookForm(request.POST)
        
            if form.is_valid():
                book = form.save(commit = True)

                
                return redirect('index')

        else:
            form = forms.BookForm()            

        diction = {
            'form': form,
        }
        return render(request, 'books/add_book.html', context = diction)
    else:
        return HttpResponse('Only accessible to staff')    

def student_reg(request):

    registered = False

    if request.method == 'POST':
        student = forms.StudentUser(request.POST)
        student_info = forms.Student(request.POST)

        if student.is_valid() and student_info.is_valid():
            student_user = student.save(commit = False)
            student_user.set_password(student_user.password)
            student_user.save()

            student_info_data = student_info.save(commit = False)
            student_info_data.user = student_user

            student_info_data.save()

            registered = True

    else:
        student = forms.StudentUser()
        student_info = forms.Student()

    diction = {
        'student': student,
        'student_info': student_info,
        'registered': registered,
    }                

    return render(request, 'books/student_reg.html', context = diction)

def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        username = User.objects.get(email = email.lower()).username

        student = authenticate(username = username, password = password)

        if student is not None:
            login(request, student)

            return redirect('student_profile')

        else:
            messages.error(request, 'Email/password incorrect')

    return render(request, 'books/student_login.html') 

@login_required
def student_profile(request):
    if request.user.is_superuser:
        users = User.objects.filter(is_superuser = False).all()

        diction = {
            'users': users,
        }
        return render(request, 'books/superuser_profile.html', context=diction)

    issued_books = IssuedBooks.objects.filter(student_id = request.user.id).all()

    
    diction = {
        'issued_books': issued_books,
    }
    return render(request, 'books/student_profile.html', context = diction) 

@login_required
def student_logout(request):

    logout(request)   

    return redirect('index')    

def book_details(request, pk):
    book = Book.objects.get(pk = pk)
    form = forms.ReviewForm()
    reviews = Review.objects.filter(book = book)
    book_issued = False
    is_staff = False

    if request.user.is_staff:
        is_staff = True

    diction = {
        'book': book,
        'form': form, 
        'reviews': reviews,
        'book_issued': book_issued,
        'is_staff': is_staff,
    }

    if request.user.is_authenticated:
        try:
            issued_books_student = IssuedBooks.objects.get(student = request.user, book = book) # Gets all the rows of books issued by the student

            if issued_books_student:
                issue_date = issued_books_student.issue_period
                time_left = datetime.timedelta(days = 14) - (datetime.datetime.now().date() - issue_date.date())
            
                diction.update({'book_issued': True, 'time_left': time_left, 'issue_details': issued_books_student})

        except:
            diction.update({'book_issued': False})        

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)

        if form.is_valid:
            review = form.save(commit=False)
            review.student = request.user
            review.book = book

            review.save()

            return redirect('index')


    return render(request, 'books/book_details.html', context = diction)

def issue_book(request, pk):
    IssuedBooks.objects.create(student = request.user, book = Book.objects.get(pk = pk), issue_period = datetime.datetime.now())

    return render(request, 'books/issue_book.html', context = {})

def renew_book(request, pk):
    IssuedBooks.objects.get(student = request.user, book = Book.objects.get(pk=pk)).delete()
    
    IssuedBooks.objects.create(student = request.user, book = Book.objects.get(pk=pk), issue_period = datetime.datetime.now())

    return render(request, 'books/renew_book.html', context = {})

def search(request):
    query = request.GET.get('query', '')
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))

    return render(request, 'books/search.html', context = {'books': books, 'query': query})

def genre_books(request, pk):
    genre = Genre.objects.get(pk=pk)

    return render(request, 'books/genre.html', context = {'genre': genre})  

def return_book(request, pk):
    IssuedBooks.objects.get(pk=pk).delete()

    return render(request, 'books/return_book.html', context={})      

def staff_reg(request):
    if request.user.is_superuser:
        form = forms.StudentUser()
        diction = {
            'form': form,
        }

        if request.method == 'POST':
            form = forms.StudentUser(request.POST)

            if form.is_valid:
                staff = form.save(commit=False)
                staff.set_password(staff.password)
                staff.is_staff = True
                staff.save()

                return redirect('index')

        return render(request, 'books/staff_reg.html', context=diction)
    else:
        return HttpResponse('Only accessible by superuser')    
    
def delete_user(request, pk):
    User.objects.get(pk=pk).delete()

    return HttpResponse('User deleted successfully')

def update_book(request, pk):
    book = Book.objects.get(pk=pk)

    if request.method == 'POST':
        form = forms.BookForm(request.POST, instance=book)

        if form.is_valid:
            updated_book = form.save(commit=True)

            return redirect('index')
    else:
        form = forms.BookForm(instance=book) 

    diction = {
        'form': form,
    }               


    return render(request, 'books/update_book.html', context=diction)
