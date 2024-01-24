from django.db import models
from django.db.models import QuerySet
from django.utils import timezone, text
from djmoney.models.fields import MoneyField
from django.core.validators import RegexValidator
from datetime import datetime


class DbItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: bool = True


class Category(DbItem):
    class Kind(models.TextChoices):
        product_taxonomy = "PT", "Таксономия продуктов"

    kind = models.CharField(max_length=2, choices=Kind.choices, default=Kind.product_taxonomy)                              # тип категории
    title = models.CharField(max_length=250)                                                                                # название категории
    description = models.TextField(null=True, blank=True)                                                                   # описание категории
    category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')     # объемлющая категория

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["title"])]

    def __str__(self):
        return self.title


class Product(DbItem):
    article = models.CharField(primary_key=True, max_length=100)                                            # внутренний артикул
    title = models.CharField(max_length=500)                                                                # название
    description = models.TextField(null=True, blank=True)                                                   # описание
    color = models.CharField(max_length=250, null=True, blank=True)                                         # цвет
    actual_price = MoneyField(max_digits=14, decimal_places=2, default_currency='RUR')                      # цена
    old_price = MoneyField(max_digits=14, decimal_places=2, default_currency='RUR', null=True, blank=True)  # старая цена (до акции), null -- нет акции
    sales_quantity = models.BigIntegerField(default=0)                                                      # количество продаж
    published_at = models.DateTimeField(null=True, blank=True, default=timezone.now)                        # время публикации(опубликован, если published_at < now())
    slug = models.SlugField(unique=True, max_length=200)                                                    # слаг
    categories = models.ManyToManyField(Category, related_name="products")                                  # категории

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = text.slugify(self.article, self.title)
        super().save(*args, **kwargs)

    class PublishedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().exclude(published_at=None).filter(published_at__lte=timezone.now())

    class BestsellersManager(PublishedManager):
        def get_queryset(self):
            return super().get_queryset().order_by('-sales_quantity')

    objects = models.Manager()
    published = PublishedManager()
    bestsellers = BestsellersManager()

    images: QuerySet                        # -- Just for IDE syntax analyzer --
    sizes: QuerySet
    attributes: QuerySet
    orders: QuerySet

    class Meta:
        ordering = ["published_at"]
        indexes = [models.Index(fields=["title"])]

    def __str__(self):
        return f"{self.article}: {self.title}"

    @property
    def primary_image(self):
        query = self.images.filter(primary=True)
        return query.first() if query.exists() else None

    @property
    def absolute_url(self):
        return ""                           # TODO -- implement me --

    @property
    def quantity(self):
        return self.sizes.aggregate(models.Sum("quantity", default=0))["quantity__sum"]

    @property
    def in_stock(self):
        return self.sizes.filter(quantity__gt=0).exists()

    @property
    def novelty(self):
        return (datetime.now().date() - self.published_at.date()).days < 30 if self.published_at else False;


class AvailableSize(DbItem):
    size = models.CharField(max_length=30)                                                  # размер
    quantity = models.BigIntegerField()                                                     # количество в наличии
    product = models.ForeignKey(Product, related_name="sizes", on_delete=models.CASCADE)    # товар

    def __str__(self):
        return self.size


class Attribute(DbItem):
    name = models.CharField(max_length=50)                                                          # имя атрибута
    value = models.CharField(max_length=250)                                                        # значение атрибута
    product = models.ForeignKey(Product, related_name="attributes", on_delete=models.CASCADE)       # товар

    def __str__(self):
        return self.name


class Image(DbItem):
    primary = models.BooleanField()                                                             # основное изображение?
    image = models.ImageField(upload_to='products/%Y/%m/%d')                                    # картинка
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)       # товар

    class PrimariesManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(primary=True)

    objects = models.Manager()
    primaries = PrimariesManager()

    def __str__(self):
        return 'изображение'


class Order(DbItem):
    scart_id = models.CharField(max_length=100)                                                 # ид.корзины
    size = models.CharField(max_length=30)                                                      # размер
    quantity = models.BigIntegerField()                                                         # количество
    product = models.ForeignKey(Product, related_name="orders", on_delete=models.CASCADE)       # товар

    def __str__(self):
        return f'заказ на {self.product} из корзины {self.scart_id}'


class NotificationRequest(DbItem):
    name = models.CharField(null=False, max_length=150)
    email = models.EmailField(null=False, max_length=250)
    phone = models.CharField(null=False, max_length=50)
    ppk = models.EmailField(null=False, max_length=100)

    def __str__(self):
        return f'Запрос #{self.id} на уведомление о поступлении товара артикул: {self.ppk}, от: {self.name}, телефон: {self.phone}, email: {self.email}'
