from rest_framework.viewsets import ModelViewSet, GenericViewSet
from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer, UserBookRelationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from store.permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsOwnerOrReadOnly]
    filterset_fields = ['price']
    search_fields = ['author_name', 'name']
    ordering_fields = ['price','author_name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBooksRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        return obj

def auth(request):
    return render(request, 'oauth.html')