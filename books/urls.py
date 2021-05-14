from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('add-book/', views.add_book, name = 'add_book'),
    path('student-reg/', views.student_reg, name = 'student_reg'),
    path('student-login/', views.student_login, name = 'student_login'),
    path('student-profile/', views.student_profile, name = 'student_profile'),
    path('student-logout/', views.student_logout, name = 'student_logout'),
    path('book-details/<pk>/', views.book_details, name = 'book_details'),
    path('issue-book/<pk>', views.issue_book, name = 'issue_book'),
    path('renew-book/<pk>', views.renew_book, name = 'renew_book'),
]
