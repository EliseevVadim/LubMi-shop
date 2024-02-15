from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'kind', 'description', 'category', 'created_at', 'updated_at']
    list_filter = ['title', 'kind', 'category', 'created_at', 'updated_at']
    search_fields = ['title']
    ordering = ['title', 'category']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'article', 'description', 'color', 'weight', 'actual_price', 'old_price', 'published_at', 'created_at', 'updated_at']
    list_filter = ['title', 'article', 'published_at']
    search_fields = ['published_at', 'article', 'title']
    ordering = ['title', 'article']
    prepopulated_fields = {'slug': ('article', 'title')}


@admin.register(AvailableSize)
class AvailableSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'quantity']
    list_filter = ['product', 'size']
    search_fields = ['size', 'quantity']
    ordering = ['product', 'size']


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'product']
    list_filter = ['name', 'value']
    search_fields = ['name', 'value']
    ordering = ['name', 'value']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'primary', 'image']
    list_filter = ['product', 'primary']
    ordering = ['product', 'primary']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['slug', 'cu_fullname', 'status']
    list_filter = ['cu_fullname', 'status']
    search_fields = ['cu_fullname']
    prepopulated_fields = {'slug': ('uuid',)}


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ['title', 'token', 'description']
    search_fields = ['title', 'size', 'quantity']
    ordering = ['title', 'token']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['bot', 'title', 'cid', 'active']
    list_filter = ['bot']
    search_fields = ['title', 'cid', 'active']
    ordering = ['active', 'title', 'cid']


@admin.register(Parameter)
class ParamAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'in_context', 'description']
    search_fields = ['key', 'value']


@admin.register(Coworker)
class CoworkerAdmin(admin.ModelAdmin):
    list_display = ['title', 'key', 'description']
    search_fields = ['title']


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'description']
    list_filter = ['owner']
    search_fields = ['key', 'value']


@admin.register(AboutItem)
class AboutItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'description', 'image', 'kind']
    list_filter = ['kind']
    search_fields = ['label']
