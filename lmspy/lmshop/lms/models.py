import uuid

from django.db import models
from django.db.models import QuerySet
from django.utils import timezone, text
from django.core.validators import MinValueValidator, RegexValidator
from djmoney.models.fields import MoneyField
from datetime import datetime


class DbItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: bool = True


class Parameter(DbItem):
    key = models.CharField(primary_key=True, max_length=50)                                     # -- ключ --
    value = models.CharField(max_length=250)                                                    # -- значение --
    in_context = models.BooleanField(default=True)                                              # -- используется в контексте --
    description = models.TextField(null=True, blank=True)                                       # -- описание --

    def __str__(self):
        return f'Параметр "{self.key}"'

    @staticmethod
    def value_of(key, default=""):
        try:
            return Parameter.objects.get(pk=key).value
        except Parameter.DoesNotExist:
            return default


class Tunable:
    @staticmethod
    def _regex_validator(rgx_key, msg_key, default_regexp, default_message):
        return RegexValidator(
            regex=Parameter.value_of(rgx_key, default_regexp),
            message=Parameter.value_of(msg_key, default_message)
        )

    @staticmethod
    def validate_size(value):
        Tunable._regex_validator(
            "regex_cloth_size",
            "message_invalid_cloth_size",
            """^(\d*(?:M|X{0,2}[SL]))(?:$|\s+.*$)""",
            "Размер не соответствует образцу"
        )(value)

    @staticmethod
    def validate_article(value):
        Tunable._regex_validator(
            "regex_article",
            "message_invalid_article",
            """[А-Яа-яЁё\w\d\-]+""",
            "Артикул не соответствует образцу"
        )(value)

    @staticmethod
    def validate_phone(value):
        Tunable._regex_validator(
            "regex_phone_number",
            "message_invalid_phone_number",
            """^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$""",
            "Номер телефона не соответствует образцу"
        )(value)


class Category(DbItem):
    class Kind(models.TextChoices):
        product_taxonomy = "pt", "Таксономия продуктов"

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
    article = models.CharField(primary_key=True, max_length=100, validators=[Tunable.validate_article])     # внутренний артикул
    title = models.CharField(max_length=100)                                                                # название
    slug = models.SlugField(unique=True, max_length=200)                                                    # слаг
    description = models.TextField(null=True, blank=True)                                                   # описание
    color = models.CharField(max_length=50, null=True, blank=True)                                          # цвет
    weight = models.BigIntegerField(validators=[MinValueValidator(0)])                                      # вес
    actual_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='RUR',
        validators=[MinValueValidator(0.01)])                                                               # цена
    old_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='RUR',
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01)])                                                               # старая цена (до акции), null -- нет акции
    sales_quantity = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])                   # количество продаж
    published_at = models.DateTimeField(null=True, blank=True, default=timezone.now)                        # время публикации(опубликован, если published_at < now())
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

    images: QuerySet                                                                            # -- Just for IDE syntax analyzer --
    sizes: QuerySet
    attributes: QuerySet
    orders: QuerySet

    class Meta:
        ordering = ["published_at"]
        indexes = [models.Index(fields=["title"])]

    def __str__(self):
        return f"{self.article}:{self.title}"

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
        return (datetime.now().date() - self.published_at.date()).days < 30 if self.published_at else False

    @property
    def variants(self):
        return {size.id: size.size for size in self.sizes.filter(quantity__gt=0).all()}


class AvailableSize(DbItem):
    size = models.CharField(max_length=30, validators=[Tunable.validate_size])                  # размер
    quantity = models.BigIntegerField(validators=[MinValueValidator(0)])                        # количество в наличии
    product = models.ForeignKey(Product, related_name="sizes", on_delete=models.CASCADE)        # товар

    class Meta:
        ordering = ["size"]
        constraints = [models.UniqueConstraint(
            fields=["size", "product_id"],
            name="unique_size_per_product"
        )]

    def __str__(self):
        return self.size


class Attribute(DbItem):
    name = models.CharField(max_length=50)                                                      # имя атрибута
    value = models.CharField(max_length=250)                                                    # значение атрибута
    product = models.ForeignKey(Product, related_name="attributes", on_delete=models.CASCADE)   # товар

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


class Region(DbItem):
    region_code = models.IntegerField(primary_key=True, editable=False)                         # -- код СДЭК --
    region = models.CharField(max_length=100)                                                   # -- название --
    country_code = models.CharField(max_length=2, default='RU')                                 # -- код страны --
    country = models.CharField(max_length=50, default='Россия')                                 # -- название страны --
    cities: QuerySet                                                                            # -- Just for IDE syntax analyzer --

    class Meta:
        ordering = ["region"]
        indexes = [models.Index(fields=["region"])]

    def __str__(self):
        return f'{self.region}'


class City(DbItem):
    city_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)          # -- ключ СДЭК --
    code = models.BigIntegerField(editable=False)                                               # -- код СДЭК --
    city = models.CharField(max_length=100)                                                     # -- название --
    city_lc = models.CharField(max_length=100)                                                  # -- название в нижнем регистре --
    country_code = models.CharField(max_length=2, default='RU')                                 # -- код страны --
    country = models.CharField(max_length=50, default='Россия')                                 # -- название страны --
    sub_region = models.CharField(max_length=100, null=True)                                    # -- район --
    longitude = models.FloatField(editable=False)                                               # -- долгота --
    latitude = models.FloatField(editable=False)                                                # -- широта --
    time_zone = models.CharField(max_length=50)                                                 # -- часовая зона --
    region = models.ForeignKey(Region,                                                          # -- регион --
                               null=True,
                               related_name="cities",
                               on_delete=models.CASCADE)

    class Meta:
        ordering = ["city"]
        indexes = [models.Index(fields=["city_lc", "city"])]

    def __str__(self):
        return f'{self.city}'

    @property
    def region_full(self):
        return f'{self.region.region if self.region else "регион неизвестен"}{", " + self.sub_region if self.sub_region else ""}'

    @property
    def city_full(self):
        return f'{self.city}, {self.region_full}'


class Order(DbItem):
    class DeliveryService(models.TextChoices):
        cd = "cd", "СДЭК"
        pr = "pr", "Почта России"

    slug = models.SlugField(unique=True, max_length=200)                                        # -- слаг --
    bank_payment_id = models.CharField(max_length=250)                                          # -- Id банковской платежки --
    closed_at = models.DateTimeField(null=True, blank=True, default=None)                       # -- время и флаг выполнения --
    city = models.ForeignKey(City, null=False, on_delete=models.PROTECT)
    delivery_service = models.CharField(                                                        # -- тип доставки --
        max_length=2,
        choices=DeliveryService.choices,
        default=DeliveryService.cd)
    delivery_cost = MoneyField(                                                                 # -- стоимость доставки --
        max_digits=14,
        decimal_places=2,
        default_currency='RUR')
    cu_name = models.CharField(max_length=250)                                                  # -- как обращаться --
    cu_phone = models.CharField(null=True, max_length=50, validators=[Tunable.validate_phone])  # -- телефон --
    cu_email = models.CharField(null=True, max_length=250)                                      # -- email --
    cu_city_uuid = models.UUIDField(null=True)                                                  # -- город --
    cu_city = models.CharField(max_length=100)                                                  # -- город --
    cu_city_region = models.CharField(null=True, max_length=100)                                # -- город --
    cu_city_subregion = models.CharField(null=True, max_length=100)                             # -- город --
    cu_street = models.CharField(max_length=200)                                                # -- улица --
    cu_building = models.CharField(max_length=50)                                               # -- здание --
    cu_entrance = models.CharField(max_length=50)                                               # -- подъезд --
    cu_floor = models.CharField(max_length=50)                                                  # -- этаж --
    cu_apartment = models.CharField(max_length=50)                                              # -- квартира/офис --
    cu_fullname = models.CharField(max_length=250)                                              # -- полное имя заказчика --
    cu_confirm = models.BooleanField(default=False)                                             # -- поставил галочку про конфиденциальность? --
    items: QuerySet                                                                             # -- компоненты, Just for IDE syntax analyzer --

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = text.slugify(self.created_at, self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'заказ #{self.slug} от {self.cu_name}'


class OrderItem(DbItem):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)                        # -- заказ --
    ppk = models.CharField(max_length=100, validators=[Tunable.validate_article])                           # -- внутренний артикул --
    title = models.CharField(max_length=150)                                                                # -- название --
    size = models.CharField(max_length=30, validators=[Tunable.validate_size])                              # -- размер --
    quantity = models.BigIntegerField(validators=[MinValueValidator(1)])                                    # -- количество --
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='RUR')                             # -- цена на момент заказа --

    def __str__(self):
        return f'{self.title} ({self.quantity})'


class NotificationRequest(DbItem):
    name = models.CharField(null=False, max_length=150)
    email = models.EmailField(null=True, max_length=250)
    phone = models.CharField(null=True, max_length=50, validators=[Tunable.validate_phone])
    ppk = models.CharField(null=False, max_length=100)

    def __str__(self):
        return f'Запрос #{self.id} на уведомление о поступлении товара артикул: {self.ppk}, от: {self.name}, телефон: {self.phone or "не указан"}, email: {self.email or "не указан"}'


class TelegramBot(DbItem):
    title = models.CharField(max_length=50)                                                     # -- название --
    description = models.TextField(null=True, blank=True)                                       # -- описание --
    token = models.CharField(max_length=150)                                                    # -- токен --
    chats: QuerySet                                                                             # -- Just for IDE syntax analyzer --

    def __str__(self):
        return f'Телеграм-бот "{self.title}"'


class Chat(DbItem):
    title = models.CharField(max_length=50)                                                     # -- название --
    cid = models.IntegerField(blank=False)                                                      # -- идентификатор чата --
    active = models.BooleanField(default=True)                                                  # -- активен? --
    bot = models.ForeignKey(TelegramBot, related_name="chats", on_delete=models.CASCADE)        # -- бот --

    def __str__(self):
        return f'Телеграм-чат "{self.title}"'


class Coworker(DbItem):
    key = models.CharField(primary_key=True, max_length=2)                                      # -- ключ --
    title = models.CharField(max_length=50)                                                     # -- название --
    description = models.TextField(null=True, blank=True)                                       # -- описание --
    settings: QuerySet                                                                          # -- Just for IDE syntax analyzer --

    def __str__(self):
        return f'"{self.title}"'

    @staticmethod
    def setting(cpk, spk, default=None):
        try:
            return Coworker.objects.get(pk=cpk).settings.get(pk=spk).value
        except Coworker.DoesNotExist:
            return default
        except Setting.DoesNotExist:
            return default


class Setting(DbItem):
    key = models.CharField(primary_key=True, max_length=32)                                     # -- ключ --
    value = models.CharField(max_length=150)                                                    # -- значение --
    description = models.TextField(null=True, blank=True)                                       # -- описание --
    owner = models.ForeignKey(Coworker, related_name="settings", on_delete=models.CASCADE)      # -- владелец --

    def __str__(self):
        return f'<{self.owner.key}>:<{self.key}>:<{self.value}>'
