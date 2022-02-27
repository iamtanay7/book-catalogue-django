import csv
import io
from multiprocessing import context
from urllib import response
from django.db import connection
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
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Authors.csv'
    writer = csv.writer(response)
    #writer.writerow(["id", "name", "age", "gender", "country", "image_url"])
    auths = authors.values_list("id", "name", "age", "gender", "country", "image_url")
    for obj in auths:
        writer.writerow(obj)
    return response
    # cursor = connection.cursor()
    # response = HttpResponse(
    #     content_type='text/csv',
    #     headers={'Content-Disposition': 'attachment; filename="Authors.csv"'},
    # )
    # writer = csv.writer(response)
    # sql = "COPY (SELECT * FROM webapp_book) TO STDOUT WITH CSV DELIMITER ','"
    # text_stream = io.StringIO()
    # cursor.copy_expert(sql, text_stream)
    # writer.writerows(text_stream.getvalue())
    # return response
    


def export_books_to_csv(request):
    books = Book.objects.all()
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=Books.csv'
    writer = csv.writer(response)
    # writer.writerow(["id", "name", "Publish date", "No of pages", "Critics rating","Author", "image_url"])
    new_books = books.values_list("id", "name", "average_critics_rating","number_of_pages", "date_of_publishing", "author_name", "image_url")
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
        book.id = Book.objects.latest("id").id+1
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

class AddNewAuthor(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        print(data)
        author = Author()
        author.id = Author.objects.latest("id").id+1
        author.name = data.get("name")
        author.age = data.get("age")
        author.gender = data.get("gender")
        author.country = data.get("country")
        author.image_url = data.get("image_url")
        try:
            author.save()
        except Exception as e:
            print(e)
            return JsonResponse({"error":"Invalid input"})
        return JsonResponse({"message":"Author Added successfully!"})


