import csv
from multiprocessing import context
from urllib import response

from django.shortcuts import render
from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


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

def export_books_to_csv(request):
    books = Book.objects.all()
    response = HttpResponse("text/csv")
    response['Content-Disposition'] = 'attachment; filename=Books.csv'
    writer = csv.writer(response)
    writer.writerow(["id", "name", "Publish date", "No of pages", "Critics rating","Author", "image_url"])
    new_books = books.values_list("id", "name", "date_of_publishing", "number_of_pages", "average_critics_rating", "author_name", "image_url")
    for obj in new_books:
        writer.writerow(obj)
    return response

class BookView(APIView):
    def get(self, request):
        data = Book.objects.all()
        for obj in data:
            obj.author_name = Author.objects.get(pk=1).name
        print(data)
        serialized_data = BookSerializer(data, many=True, context={"request": request})
        return JsonResponse(serialized_data.data, safe=False)

class AllAuthorsView(APIView):
    def get(self, request):
        data = Author.objects.all()
        res = []
        for author in data:
            res.append({"id":author.id,"name":author.name})
        return JsonResponse(res, safe=False)

class AddNewBook(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        print(data)
        book = Book()
        book.author = Author.objects.get(pk=data.get("author_id") )
        book.number_of_pages = data.get("number_of_pages")
        book.date_of_publishing = data.get("date_of_publishing")
        book.author_name = Author.objects.get(pk=data.get("author_id")).name
        book.name = data.get("name")
        book.image_url = data.get("image_url")
        book.average_critics_rating = data.get("average_critics_rating")
        try:
            book.save()
        except Exception as e:
            print(e)
            return JsonResponse({"error":"Invalid input"})
        return JsonResponse({"message":"Book Added successfully!"})


