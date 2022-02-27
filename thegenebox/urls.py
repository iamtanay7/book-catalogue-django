"""thegenebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from webapp.views import AddNewBook, AuthorViewSet, BookViewSet, export_authors_to_csv, BookView, AllAuthorsView, AddNewBook, export_books_to_csv, AddNewAuthor

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('exportauthorsascsv/', export_authors_to_csv),
    path('exportbooksascsv/', export_books_to_csv),
    path('booksapi/', BookView.as_view()),
    path('allauthors/', AllAuthorsView.as_view()),
    path('addnewbook/', AddNewBook.as_view()),
    path('addnewauthor/', AddNewAuthor.as_view())
]
