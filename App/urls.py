import imp
from django.contrib import admin
from django.urls import path,include
from App import views
import App
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login,name='login'),
    path('register',views.register,name='register'),
    path('home',views.home,name='home'),
    path('newUser',views.newUser,name='newUser'),
    # path('Admin',views.Admin,name='Admin'),
    path('Otp',views.Otp,name='Otp'),
    path('OtpVari',views.OtpVari,name='OtpVari'),
    path('error',views.error,name='error'),
    path('insertBook',views.insertBook,name='insertBook'),
    path('searchBook',views.searchBook,name='searchBook'),
    path('insert',views.insert,name='insert'),
    path('search',views.search,name='search'),
    path('profile',views.profile,name='profile'),
    path('issueBook',views.issueBook,name='issueBook'),
    path('returnBook',views.returnBook,name='returnBook'),
    path('ReturnBook_list',views.ReturnBook_list,name='ReturnBook_list'),
    path('return_issue_book',views.return_issue_book,name='return_issue_book'),
    path('history',views.history,name='history'),
    path('BookHistory_list',views.BookHistory_list,name='BookHistory_list'),
    path('LogOut',views.LogOut,name='LogOut'),
    path('FeedSubmit',views.FeedSubmit,name='FeedSubmit'),
    path('FeedbackList',views.FeedbackList,name='FeedbackList'),
    path('Feedback_list',views.Feedback_list,name='Feedback_list'),
    path('AboutUs',views.AboutUs,name='AboutUs'),
    path('Ebooks',views.Ebooks,name='Ebooks'),
    path('EbooksBookName',views.EbooksBookName,name='EbooksBookName'),
    path('Ebook_list',views.Ebook_list,name='Ebook_list'),
    path('news',views.news,name='news'),
    path('newsList',views.newsList,name='newsList')
]