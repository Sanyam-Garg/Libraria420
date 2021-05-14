from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book, Review, Student, IssuedBooks
from . import forms

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from datetime import date

# Create your views here.
def index(request):
    books = Book.objects.order_by('title').all()

    diction = {
        'books': books,
    }
    return render(request, 'books/index.html', context = diction)

def add_book(request):

    if request.method == 'POST':
        form = forms.BookForm(request.POST)
        
        if form.is_valid():
            book = form.save(commit = False)

            if 'cover' in request.FILES:
                book.cover = request.FILES['cover']

                book.save()

                return redirect('index')

    else:
        form = forms.BookForm()            

    diction = {
        'form': form,
    }
    return render(request, 'books/add_book.html', context = diction)

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
            if 'profile_pic' in request.FILES:
                student_info_data.profile_pic = request.FILES['profile_pic']

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

    diction = {
        'book': book,
        'form': form, 
        'reviews': reviews,
        'book_issued': book_issued
    }

    if request.user.is_authenticated:
        issued_books_student = IssuedBooks.objects.filter(student = request.user, book = book) # Gets all the rows of books issued by the student

        if issued_books_student:
            # issue_date = issued_books_student.issue_period
            # print(issue_date)
            diction.update({'book_issued': True})

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)

        if form.is_valid:
            review = form.save(commit=False)
            review.student = request.user
            review.book = book

            review.save()

            return redirect('index')

       

    # if request.user.is_authenticated:
    #     student = request.user
    #     issued_books = IssuedBooks.objects.filter(student_id = student.id)

    #     if book in issued_books:
    #         return HttpResponse('You have already issued this book.')

    # user = request.user
    # issue_date = user.student_issue.issue_period.date()
    # diction.update({
    #     'issue_date':issue_date,
    # })
    
          
    # if request.method == 'POST':
    #     IssuedBooks.objects.create(student_id = request.user.id, book_id = book.id)


    return render(request, 'books/book_details.html', context = diction)

def issue_book(request, pk):
    IssuedBooks.objects.create(student = request.user, book = Book.objects.get(pk = pk))

    return render(request, 'books/issue_book.html', context = {})


