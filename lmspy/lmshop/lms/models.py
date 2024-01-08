from django.db import models
from django.utils import timezone


class DbItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: bool = True


# Create your models here.
class Category(DbItem):
    class Kind(models.TextChoices):
        product_taxonomy = "PT", "Таксономия продуктов"

    kind = models.CharField(max_length=2, choices=Kind.choices, default=Kind.product_taxonomy)                  # тип категории
    title = models.CharField(max_length=250)                                                                    # название категории
    description = models.TextField(null=True)                                                                   # описание категории
    category = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='subcategories')     # объемлющая категория

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["title"])]

    def __str__(self):
        return self.title


class Product(DbItem):
    article = models.CharField(primary_key=True, max_length=250)                    # внутренний артикул, он же идентификатор
    title = models.CharField(max_length=500)                                        # название
    description = models.TextField(null=True)                                       # описание
    color = models.CharField(max_length=250, null=True)                             # цвет
    actual_price = models.BigIntegerField()                                         # цена в копейках
    old_price = models.BigIntegerField(null=True)                                   # старая цена (до акции) в копейках
    sales_quantity = models.BigIntegerField(default=0)                              # количество продаж
    published_at = models.DateTimeField(null=True, default=timezone.now)            # время публикации(опубликован, если published_at < now())
    categories = models.ManyToManyField(Category, related_name="products")          # категории

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["title"])]

    def __str__(self):
        return self.title


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
    class Format(models.TextChoices):
        jpg = "JPG", "JPEG"
        png = "PNG", "PNG"
        gif = "GIF", "GIF"

    primary = models.BooleanField()                                                             # основное изображение?
    format = models.CharField(max_length=3, choices=Format.choices, default=Format.jpg)         # формат картинки
    image = models.TextField()                                                                  # данные, base64
    thumbnail = models.TextField(null=True)                                                     # миниатюра, base64
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)       # товар

    def __str__(self):
        return 'изображение'


class Order(DbItem):
    scart_id = models.CharField(max_length=100)                                                 # ид.корзины
    size = models.CharField(max_length=30)                                                      # размер
    quantity = models.BigIntegerField()                                                         # количество
    product = models.ForeignKey(Product, related_name="orders", on_delete=models.CASCADE)       # товар

    def __str__(self):
        return f'заказ на {self.product} из корзины {self.scart_id}'


