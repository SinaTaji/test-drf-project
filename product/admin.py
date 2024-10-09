from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active')
    list_editable = ('is_active', 'price')
    search_fields = ('title',)
    list_filter = ('is_active',)
    ordering = ('title',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(models.ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_sub')
    list_editable = ('is_sub',)
    search_fields = ('title',)
    list_filter = ('is_sub',)
    ordering = ('title',)
    prepopulated_fields = {"slug": ("title",)}
