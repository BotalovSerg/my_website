from django.contrib import admin
from store.models import Book
from django.contrib.admin import ModelAdmin


# Register your models here.
#admin.site.register(Book)

@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass