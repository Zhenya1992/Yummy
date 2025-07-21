from django.contrib import admin
from .models import Users, Categories, Products


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'telegram', 'phone',)
    search_fields = ('name', 'phone',)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):

    list_display = ('id', 'category_name')
    search_fields = ('id',)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):

    list_display = ('id', 'product_name', 'description', 'price', 'category')
    search_fields = ('id', 'price', 'category')