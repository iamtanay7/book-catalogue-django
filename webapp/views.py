import csv

from django.shortcuts import render
from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django.http import HttpResponse


# Create your views here.

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


def export_authors_to_csv(request):
    authors = Author.objects.all()
    response = HttpResponse("text/csv")
    response['Content-Disposition'] = 'attachment; filename=Authors.csv'
    writer = csv.writer(response)
    writer.writerow(["id", "name", "age", "gender", "country", "image_url"])
    auths = authors.values_list("id", "name", "age", "gender", "country", "image_url")
    for obj in auths:
        writer.writerow(obj)
    return response
