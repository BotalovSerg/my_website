from rest_framework.viewsets import ModelViewSet
from store.models import Book
from store.serializers import BooksSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render


# Create your views here.
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['price']
    search_fields = ['author_name', 'name']
    ordering_fields = ['price','author_name']

def auth(request):
    return render(request, 'oauth.html')