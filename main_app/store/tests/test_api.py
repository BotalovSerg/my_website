import json
from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer
from rest_framework import status
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg



class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.book_1 = Book.objects.create(name='Test book 1', price=100, author_name='Author 1',
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=99, author_name='Author')
        self.book_3 = Book.objects.create(name='Test book of Author 1', price=99, author_name='Author 3')

    def test_get(self):        
        url = reverse('book-list')
        #print(url)
        response = self.client.get(url)
        books = Book.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                            rating=Avg('userbookrelation__rate')).select_related('owner').prefetch_related('readers').order_by('id')
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        #print(response.data)

    def test_get_search(self):
        url = reverse('book-list')
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                                                                      rating=Avg('userbookrelation__rate'))        
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        books = Book.objects.filter(id__in=[self.book_2.id, self.book_3.id]).annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                                                                      rating=Avg('userbookrelation__rate')).select_related('owner').prefetch_related('readers').order_by('id')        
        response = self.client.get(url, data={'price': 99})
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
    
    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            "name": "Test 1",
            "price": 999,
            "author_name": "Author 1"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 999,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(999, self.book_1.price)

    def test_update_not_owner(self):
        self.user_2 = User.objects.create(username='test_user_2')
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 999,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(100, self.book_1.price)
        

    def test_update_not_owner_but_staff(self):
        self.user_2 = User.objects.create(username='test_user_2', is_staff=True)
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 999,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(999, self.book_1.price)



class BooksRelationTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username='username_1')
        self.user_2 = User.objects.create(username='username_2')

        self.book_1 = Book.objects.create(name='Test book 1', price=100, author_name='Author 1',
                                          owner=self.user_1)
        self.book_2 = Book.objects.create(name='Test book 2', price=99, author_name='Author')
        

    def test_like(self):        
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            'like': True,
        }
        json_data = json.dumps(data)        
        self.client.force_login(self.user_1)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user_1,
                                                book=self.book_1)
        self.assertTrue(relation.like)        
        
        