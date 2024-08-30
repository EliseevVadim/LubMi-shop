import uuid

from django.db import models
from django.db.models import QuerySet, F, Sum
from django.utils import timezone, text
from django.core.validators import MinValueValidator, RegexValidator
from django.conf import settings
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from lms.d6y import D6Y


class DbItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: bool = True


class Parameter(DbItem):
    key = models.CharField(primary_key=True, max_length=50)                                     # -- ключ --
    value = models.CharField(max_length=350)                                                    # -- значение --
    in_context = models.BooleanField(default=True)                                              # -- используется в контексте --
    description = models.TextField(null=True, blank=True)                                       # -- описание --

    def __str__(self):
        return f'Параметр "{self.key}"'

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"

    @staticmethod
    def value_of(key, default=""):
        try:
            return Parameter.objects.get(pk=key).value
        except Parameter.DoesNotExist:
            return default

    @staticmethod
    def construct_from_value_of(key, constructor, default):
        try:
            return constructor(Parameter.objects.get(pk=key).value)
        except (ValueError, Parameter.DoesNotExist):
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
            "Размер не соответствует образцу")(value)

    @staticmethod
    def validate_article(value):
        Tunable._regex_validator(
            "regex_article",
            "message_invalid_article",
            """[А-Яа-яЁё\w\d\-]+""",
            "Артикул не соответствует образцу")(value)

    @staticmethod
    def validate_phone(value):
        Tunable._regex_validator(
            "regex_phone_number",
            "message_invalid_phone_number",
            """^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$""",
            "Номер телефона не соответствует образцу")(value)


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
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Product(DbItem):
    article = models.CharField(primary_key=True, max_length=100, validators=[Tunable.validate_article])     # внутренний артикул
    title = models.CharField(max_length=100)                                                                # название
    slug = models.SlugField(unique=True, max_length=200)                                                    # слаг
    description = models.TextField(null=True, blank=True)                                                   # описание
    color = models.CharField(max_length=50, null=True, blank=True)                                          # цвет
    weight = models.BigIntegerField(validators=[MinValueValidator(0)])                                      # вес, в граммах
    actual_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='RUR',
        validators=[MinValueValidator(Money(0.01, currency='RUR'))])                                  # цена
    old_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='RUR',
        null=True,
        blank=True,
        validators=[MinValueValidator(Money(0.01, currency='RUR'))])                                  # старая цена (до акции), null -- нет акции
    sales_quantity = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])                   # количество продаж
    published_at = models.DateTimeField(null=True, blank=True, default=timezone.now)                        # время публикации(опубликован, если published_at < now())
    categories = models.ManyToManyField(Category, related_name="products")                                  # категории
    images: QuerySet                                                                                        # -- Just for IDE syntax analyzer --
    sizes: QuerySet
    attributes: QuerySet

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = text.slugify(self.article)
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

    class Meta:
        ordering = ["published_at"]
        indexes = [models.Index(fields=["title"])]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.article}: {self.title}"

    @property
    def primary_image(self):
        query = self.images.filter(primary=True)
        return query.first() if query.exists() else None

    @property
    def quantity(self):
        return self.sizes.aggregate(models.Sum("quantity", default=0))["quantity__sum"]

    @property
    def in_stock(self):
        return self.sizes.filter(quantity__gt=0).exists()

    @property
    def novelty(self):
        return (timezone.now().date() - self.published_at.date()).days < 30 if self.published_at else False

    @property
    def variants_in_stock(self):
        return {size.id: size.size for size in self.sizes.filter(quantity__gt=0)}

    @property
    def variants(self):
        return {size.id: size.size for size in self.sizes.all()}


class AvailableSize(DbItem):
    size = models.CharField(max_length=30, validators=[Tunable.validate_size])                  # размер
    order_value = models.IntegerField(default=0)                                                # поле для сортировки
    quantity = models.BigIntegerField(validators=[MinValueValidator(0)])                        # количество в наличии
    product = models.ForeignKey(Product, related_name="sizes", on_delete=models.CASCADE)        # товар

    class Meta:
        ordering = ['order_value']
        constraints = [
            models.UniqueConstraint(fields=["size", "product_id"], name="unique_size_per_product"),
            models.CheckConstraint(check=models.Q(quantity__gte=0), name="quantity_no_negative")]
        verbose_name = "Доступный размер"
        verbose_name_plural = "Доступные размеры"

    def __str__(self):
        return self.size


class Attribute(DbItem):
    name = models.CharField(max_length=50)                                                      # имя атрибута
    value = models.CharField(max_length=250)                                                    # значение атрибута
    product = models.ForeignKey(Product, related_name="attributes", on_delete=models.CASCADE)   # товар

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"


class Image(DbItem):
    primary = models.BooleanField()                                                             # основное изображение?
    image = models.ImageField(upload_to='products/%Y/%m/%d')                                    # картинка
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)       # товар

    class PrimariesManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(primary=True)

    objects = models.Manager()
    primaries = PrimariesManager()

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

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
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

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
        verbose_name = "Населённый пункт"
        verbose_name_plural = "Населённые пункты"

    def __str__(self):
        return f'{self.city}'

    @property
    def region_full(self):
        return f'{self.region.region if self.region else "регион неизвестен"}{", " + self.sub_region if self.sub_region else ""}'

    @property
    def city_full(self):
        return f'{self.city}{(", " + self.region_full) if self.region_full.lower() != self.city.lower() else ""}'


class Order(DbItem):
    class DeliveryService(models.TextChoices):
        cd = D6Y.CD, "СДЭК (до двери)"
        cp = D6Y.CP, "СДЭК (ПВЗ)"
        pr = D6Y.PR, "Почта России"

    class Status(models.IntegerChoices):
        pending = 0, "Создан",
        payment_paid = 1, "Оплачен",
        payment_canceled = 2, "Платёж провален",
        completed = 3, "Выполнен",

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)                               # -- UUID заказа --
    slug = models.SlugField(unique=True, max_length=100)                                        # -- слаг --
    status = models.IntegerField(choices=Status.choices, default=Status.pending)                # -- статус заказа ---
    payment_id = models.UUIDField(null=True)                                                    # -- Id банковской платежки --
    payment_json = models.TextField(null=True, blank=True)                                      # -- описание --
    completed_at = models.DateTimeField(null=True, blank=True, default=None)                    # -- время и флаг выполнения --
    city = models.ForeignKey(City, null=False, on_delete=models.PROTECT)                        # -- город - источник заказа --
    delivery_service = models.CharField(                                                        # -- тип доставки --
        max_length=2,
        choices=DeliveryService.choices,
        default=DeliveryService.cd)
    delivery_cost = MoneyField(                                                                 # -- стоимость доставки --
        max_digits=14,
        decimal_places=2,
        default_currency='RUR')
    delivery_order_json = models.TextField(null=True, blank=True)                               # -- данные заказа на доставку --
    delivery_supplements_json = models.TextField(null=True, blank=True)                         # -- дополнительные данные заказа на доставку --
    delivery_supplements_file = models.BinaryField(null=True, blank=True)                       # -- файл дополнительных данных заказа на доставку --
    delivery_point = models.CharField(null=True, max_length=15)                                 # -- код ПВЗ СДЭК или отделения Почты России
    cu_first_name = models.CharField(max_length=150)                                            # -- имя --
    cu_last_name = models.CharField(max_length=150)                                             # -- фамилия --
    cu_phone = models.CharField(null=True, max_length=50, validators=[Tunable.validate_phone])  # -- телефон --
    cu_email = models.CharField(null=True, max_length=250)                                      # -- email --
    cu_country = models.CharField(max_length=2, default='RU')                                   # -- код страны --
    cu_city_uuid = models.UUIDField(null=True)                                                  # -- город --
    cu_city = models.CharField(max_length=100)                                                  # -- город --
    cu_city_region = models.CharField(null=True, max_length=100)                                # -- регион --
    cu_city_subregion = models.CharField(null=True, max_length=100)                             # -- район --
    cu_street = models.CharField(null=True, max_length=200)                                     # -- улица --
    cu_building = models.CharField(null=True, max_length=50)                                    # -- здание --
    cu_entrance = models.CharField(null=True, max_length=50)                                    # -- подъезд --
    cu_floor = models.CharField(null=True, max_length=50)                                       # -- этаж --
    cu_apartment = models.CharField(null=True, max_length=50)                                   # -- квартира/офис --
    cu_fullname = models.CharField(max_length=250)                                              # -- полное имя заказчика --
    cu_confirm = models.BooleanField(default=False)                                             # -- поставил галочку про конфиденциальность? --
    items: QuerySet                                                                             # -- компоненты, Just for IDE syntax analyzer --

    class OrdersByStatusManager(models.Manager):
        @property
        def status(self):
            return None

        def get_queryset(self):
            return super().get_queryset().filter(status=self.status)

    class PendingManager(OrdersByStatusManager):
        @property
        def status(self):
            return Order.Status.pending

    class PaidManager(OrdersByStatusManager):
        @property
        def status(self):
            return Order.Status.payment_paid

    class CanceledManager(OrdersByStatusManager):
        @property
        def status(self):
            return Order.Status.payment_canceled

    class CompletedManager(OrdersByStatusManager):
        @property
        def status(self):
            return Order.Status.completed

    objects = models.Manager()
    pending = PendingManager()
    paid = PaidManager()
    canceled = CanceledManager()
    completed = CompletedManager()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = text.slugify(self.uuid)
        super().save(*args, **kwargs)

    @property
    def total_price_with_delivery(self):
        return Money(self.items.aggregate(total=Sum(F("price") * F('quantity')))["total"] + self.delivery_cost.amount, currency="RUR")

    @property
    def total_price_without_delivery(self):
        return Money(self.items.aggregate(total=Sum(F("price") * F('quantity')))["total"], currency="RUR")

    @property
    def total_price(self):
        return self.total_price_without_delivery if settings.PREFERENCES.D6yPaymentUponReceipt else self.total_price_with_delivery

    @property
    def total_weight(self):
        return self.items.aggregate(total=Sum(F("weight") * F('quantity')))["total"]

    @property
    def total_units(self):
        return self.items.aggregate(total=Sum(F('quantity')))["total"]

    @property
    def delivery_address(self):
        def o(prefix, value):
            nonlocal items
            items += [f'{prefix}: {value}'] if value and value != str(None) else []
        items = []
        o('Нас. пункт', self.cu_city),
        o('Улица', self.cu_street),
        o('Здание', self.cu_building),
        o('Подъезд', self.cu_entrance),
        o('Этаж', self.cu_floor),
        o('Квартира/офис', self.cu_apartment)
        o('Пункт выдачи', self.delivery_point)
        return ", ".join(items)

    @property
    def delivery_address_short(self):
        def o(prefix, value):
            nonlocal items
            items += [f'{prefix}. {value}'] if value and value != str(None) else []
        items = [f'{self.cu_city}', f'{self.cu_street}']
        o('д', self.cu_building)
        o('кв', self.cu_apartment)
        return ", ".join(items)

    @property
    def delivery_address_in_city(self):
        def o(prefix, value):
            nonlocal items
            items += [f'{prefix}. {value}'] if value and value != str(None) else []
        items = [f'{self.cu_street}']
        o('д', self.cu_building)
        o('кв', self.cu_apartment)
        return ", ".join(items)

    @property
    def delivery_cost_cents(self):
        return int(self.delivery_cost.amount * 100)

    @property
    def width(self):
        return Parameter.construct_from_value_of("value_package_width", int, settings.PACKAGE_WIDTH_CM)

    @property
    def length(self):
        return Parameter.construct_from_value_of("value_package_length", int, settings.PACKAGE_LENGTH_CM)

    @property
    def height(self):
        return Parameter.construct_from_value_of("value_package_unit_height", int, settings.PACKAGE_UNIT_HEIGHT_CM) * self.total_units

    def __str__(self):
        return f'заказ #{self.slug} от {self.cu_first_name}'


class OrderItem(DbItem):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)                        # -- заказ --
    product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT)                               # -- продукт --
    ppk = models.CharField(max_length=100, validators=[Tunable.validate_article])                           # -- внутренний артикул --
    title = models.CharField(max_length=150)                                                                # -- название --
    size = models.CharField(max_length=30, validators=[Tunable.validate_size])                              # -- размер --
    quantity = models.BigIntegerField(validators=[MinValueValidator(1)])                                    # -- количество --
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='RUR')                             # -- цена на момент заказа --
    weight = models.BigIntegerField(validators=[MinValueValidator(0)])                                      # -- вес, в граммах --

    class Meta:
        constraints = [models.CheckConstraint(check=models.Q(quantity__gt=0), name="quantity_positive")]
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"

    @property
    def color(self):
        return (self.product.color or "Не указан") if self.product else "Недоступен"

    @property
    def price_cents(self):
        return int(self.price.amount * 100)

    @property
    def amount_cents(self):
        return self.price_cents * self.quantity

    def __str__(self):
        return f'{self.title} ({self.quantity})'


class NotificationRequest(DbItem):
    name = models.CharField(null=False, max_length=150)
    email = models.EmailField(null=True, max_length=250)
    phone = models.CharField(null=True, max_length=50, validators=[Tunable.validate_phone])
    ppk = models.CharField(null=False, max_length=100)
    size = models.CharField(null=True, max_length=30)

    def __str__(self):
        return f'Запрос #{self.id} на уведомление о поступлении товара артикул: `{self.ppk}`, размер: `{self.size or "не указан"}` от: `{self.name}`, телефон: `{self.phone or "не указан"}`, email: `{self.email or "не указан"}`'

    class Meta:
        verbose_name = "Запрос уведомления"
        verbose_name_plural = "Запросы уведомления"


class TelegramBot(DbItem):
    title = models.CharField(max_length=50)                                                     # -- название --
    description = models.TextField(null=True, blank=True)                                       # -- описание --
    token = models.CharField(max_length=150)                                                    # -- токен --
    chats: QuerySet                                                                             # -- Just for IDE syntax analyzer --

    class Meta:
        verbose_name = "Telegram-бот"
        verbose_name_plural = "Telegram-боты"

    def __str__(self):
        return f'Телеграм-бот "{self.title}"'


class Chat(DbItem):
    title = models.CharField(max_length=50)                                                     # -- название --
    cid = models.IntegerField(blank=False)                                                      # -- идентификатор чата --
    active = models.BooleanField(default=True)                                                  # -- активен? --
    bot = models.ForeignKey(TelegramBot, related_name="chats", on_delete=models.CASCADE)        # -- бот --

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    def __str__(self):
        return f'Телеграм-чат "{self.title}"'


class Coworker(DbItem):
    key = models.CharField(primary_key=True, max_length=2)                                      # -- ключ --
    title = models.CharField(max_length=50)                                                     # -- название --
    description = models.TextField(null=True, blank=True)                                       # -- описание --
    settings: QuerySet                                                                          # -- Just for IDE syntax analyzer --

    def __str__(self):
        return f'"{self.title}"'

    class Meta:
        verbose_name = "Служба"
        verbose_name_plural = "Службы"

    @staticmethod
    def setting(cpk, skey, default=None):
        try:
            return Coworker.objects.get(pk=cpk).settings.get(key=skey).value
        except (Coworker.DoesNotExist, Setting.DoesNotExist):
            return default


class Setting(DbItem):
    key = models.CharField(max_length=32)                                                       # -- ключ --
    value = models.CharField(max_length=150)                                                    # -- значение --
    description = models.TextField(null=True, blank=True)                                       # -- описание --
    owner = models.ForeignKey(Coworker, related_name="settings", on_delete=models.CASCADE)      # -- владелец --

    class Meta:
        ordering = ["key"]
        indexes = [models.Index(fields=["key"])]
        constraints = [models.UniqueConstraint(
            fields=["key", "owner_id"],
            name="unique_key_per_owner"
        )]
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"

    def __str__(self):
        return f'<{self.owner.key}>:<{self.key}>:<{self.value}>'


class AboutItem(DbItem):
    class Kind(models.IntegerChoices):
        elector = 0, "Выбрал нас",
        partner = 1, "Партнёр",

    image = models.ImageField(upload_to='brand/%Y/%m/%d')                                   # -- картинка --
    label = models.CharField(max_length=50)                                                 # -- название --
    description = models.CharField(max_length=50)                                           # -- описание --
    kind = models.IntegerField(choices=Kind.choices, default=Kind.elector)                  # -- тип --
    link = models.URLField(max_length=512, default="")                                      # -- ссылка --

    class ElectoratesManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(kind=AboutItem.Kind.elector)

    class PartnersManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(kind=AboutItem.Kind.partner)

    objects = models.Manager()
    electorates = ElectoratesManager()
    partners = PartnersManager()

    class Meta:
        verbose_name = """"О бренде" - элемент"""
        verbose_name_plural = """"О бренде" - элементы"""

    def __str__(self):
        return 'Элемент информации о бренде'
