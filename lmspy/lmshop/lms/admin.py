from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

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
    list_filter = ['title', 'published_at']
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
    list_display = ['cu_fullname', 'slug', 'status', 'total_price', 'items_link', 'details']
    list_filter = ['cu_fullname', 'status']
    search_fields = ['cu_fullname']
    prepopulated_fields = {'slug': ('uuid',)}

    def items_link(self, order):
        count = order.items.count()
        url = f"""{reverse("admin:lms_orderitem_changelist")}?{urlencode({"order_id": f"{order.uuid}"})}"""
        return format_html('<a href="{}">Позиции ({})</a>', url, count)

    def details(self, order):
        url = f"""{reverse("lms:admin_order_details", args=[order.slug])}"""
        return format_html('<a href="{}">Детали</a>', url)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'size', 'quantity', 'price']


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
