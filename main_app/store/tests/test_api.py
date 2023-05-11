from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Book
from store.serializers import BooksSerializer
from rest_framework import status


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(name='Test book 1', price=100, author_name='Author 1')
        self.book_2 = Book.objects.create(name='Test book 2', price=99, author_name='Author')
        self.book_3 = Book.objects.create(name='Test book of Author 1', price=150, author_name='Author 3')

    def test_get(self):        
        url = reverse('book-list')
        #print(url)
        response = self.client.get(url)
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        #print(response.data)

    def test_get_search(self):
        url = reverse('book-list')        
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')        
        response = self.client.get(url, data={'price': 99})
        serializer_data = BooksSerializer([self.book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        