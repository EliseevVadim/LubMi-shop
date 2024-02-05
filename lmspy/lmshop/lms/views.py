import decimal

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views import View
from django.template.defaultfilters import floatformat
from customerinfo.customerinfo import CustomerInfo, with_actual_scart_records_and_price
from .models import *
from .forms import ShortCustomerInfoForm, CheckoutForm


# -------------------------------------------------------------------------
# -- Main views --

class IndexView(View):
    page_size = 10
    default_order = 'novelties-first'
    ordering = {
        default_order: ("Порядок: по умолчанию", lambda q: q.order_by('-published_at')),  # TODO -- move labels to parameters! --
        'price-asc': ("Цена: по возрастанию", lambda q: q.order_by('actual_price')),
        'price-dsc': ("Цена: по убыванию", lambda q: q.order_by('-actual_price')),
        'title-asc': ("Название: А-Я", lambda q: q.order_by('title')),
        'title-dsc': ("Название: Я-А", lambda q: q.order_by('-title')),
    }

    @property
    def template_name(self):
        return 'lms/index.html'

    def get(self, request, *_, **__):
        page = request.GET.get('page')
        order = request.GET.get('order')
        order = order if order in IndexView.ordering else IndexView.default_order
        products = IndexView.ordering[order][1](Product.published.all())
        bestsellers = Product.bestsellers.all()
        pd_pgn = Paginator(products, IndexView.page_size)
        bs_pgn = Paginator(bestsellers, IndexView.page_size)
        favorites = CustomerInfo(request).favorites

        if not page:
            return render(request, self.template_name, {
                'page_title': Parameter.value_of("title_main_page", "Главная"),
                'products': pd_pgn.page(1),
                'bestsellers': bs_pgn.page(1),
                'product_pages': pd_pgn.num_pages,
                'bestseller_pages': bs_pgn.num_pages,
                'order': order,
                'order_variants': {order_value: order_item[0] for order_value, order_item in IndexView.ordering.items()},
                'favorites': favorites,
                'scui_form': ShortCustomerInfoForm(),
            })

        match request.GET.get('kind'):
            case 'bs':
                pgn = bs_pgn
            case _:
                pgn = pd_pgn

        try:
            return render(request, 'lms/plist.html', {
                'products': pgn.page(page),
                'favorites': favorites,
            })
        except PageNotAnInteger:
            return HttpResponse('')
        except EmptyPage:
            return HttpResponse('')
        except ValueError:
            return HttpResponse('')


class CatalogueView(IndexView):
    @property
    def template_name(self):
        return 'lms/catalogue.html'


class CareView(View):
    @staticmethod
    def get(request, *_, **__):
        title = Parameter.value_of('title_care', 'Уход')
        return render(request, 'lms/care.html', {
            'page_title': title,
            'page_content': 'care-page',
            'text_00': """#Уход за изделиями""",
            'text_01': """##Стирка:\n\n- Только в деликатном режиме, температура нагретой воды не должна превышать 30°
            \n\n- Не забудьте добавить кондиционер, благодаря ему ткань будет сохранять свою мягкость и упругость, а также шелк 
            не потеряет свой цвет или принт. Плюсом кондиционера станет и снижение уровня накопления электрического заряда ткани.
            \n\n- Не используйте агрессивные моющие средства. Изучите составы, чтобы в них не было отбеливателя.\n\n- Исключите отжим, 
            для удаления влаги из ткани\n\n    - Остатки влаги можно убрать махровым полотенцем.\n\n    - Можете повесить ткань на сушилку 
            и просто дать испариться воде.\n\n- Прополощите ткань в холодной воде.\n\n- Ни в коем случае не трите пятна порожком или 
            пятновыводителем.\n\n##Глажка:\n\n- Настройте температуру утюга не выше 150С;\n\n- Начните глажку с небольшого и незаметного 
            элемента вашей вещи, чтоб проверить реакции;\n\n- Лучше приступать к глажке, когда изделие не полностью высохло, и гладить через 
            другую, более плотную ткань;\n\n- Гладьте только изнаночную сторону, можете гладить на лицевой только некоторые элементы и 
            через плотную ткань; \n\n- Работайте руками быстро, не задерживайтесь с утюгом на месте;\n\n- Не используйте парогенератор."""})


class ContactsView(ListView):
    queryset = Product.published.all()
    context_object_name = 'products'
    paginate_by = 3
    template_name = 'lms/under_work.html'


class AboutCompanyView(View):
    @staticmethod
    def get(request, *_, **__):
        title = Parameter.value_of('title_about_company', 'О бренде')
        return render(request, 'lms/about.html', {
            'page_title': title,
            'page_content': 'about-page',
            'text_00': """#О бренде""",
            'text_01': """Бренд LubMi – молодой российский бренд. \n\nЭто бренд, зародившийся в мечтах маленькой девочки, которая, рисуя наряды своим
            куклам фантазировала о собственной коллекции одежды. И теперь, когда девочка выросла, её мечта осуществилась! \n\nГлавная цель создателя 
            Бренда LubMi – Любавы, это помочь в осуществлении девичьих желаний, ведь каждая девушка и женщина желает чувствовать себя красивой, утонченной,
            элегантной, женственной в любое время и в любом месте.\n\nОдеваться красиво, чувствовать себя уверенно в образах, которые еще больше 
            подчеркивают природную женскую красоту – это всё о бренде LubMi.\n\nНадевая одежду от LubMi вы проявляете истинную любовь к себе!""",
            'text_02': """##Нас выбирают""",
            'text_03': """##Партнеры""",
            'electors': [
                {
                    'img': 'pic-08.jpg',
                    'label': '**Анна Иванова**',
                    'description': 'стилист, блогер',
                },
                {
                    'img': 'pic-08.jpg',
                    'label': '**Анна Иванова**',
                    'description': 'стилист, блогер',
                },
                {
                    'img': 'pic-08.jpg',
                    'label': '**Анна Иванова**',
                    'description': 'стилист, блогер',
                },
                {
                    'img': 'pic-08.jpg',
                    'label': '**Анна Иванова**',
                    'description': 'стилист, блогер',
                },
                {
                    'img': 'pic-08.jpg',
                    'label': '**Анна Иванова**',
                    'description': 'стилист, блогер',
                },
                {
                    'img': 'pic-08.jpg',
                    'label': '**Анна Иванова**',
                    'description': 'стилист, блогер',
                },
            ],
            'partners': [
                {
                    'img': 'rosoil.jpg',
                },
                {
                    'img': 'rosoil.jpg',
                },
                {
                    'img': 'rosoil.jpg',
                },
                {
                    'img': 'rosoil.jpg',
                },
                {
                    'img': 'rosoil.jpg',
                },
                {
                    'img': 'rosoil.jpg',
                },
            ]
        })


# -------------------------------------------------------------------------
# -- Backstage views --

class ProductView(DetailView):
    model = Product
    queryset = Product.published.all()
    template_name = 'lms/pcard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorites = CustomerInfo(self.request).favorites
        return context | {
            'favorites': favorites,
        }


class SzChartView(View):
    @staticmethod
    def get(request, *_, **__):
        title = Parameter.value_of('title_size_chart', 'Таблица размеров')
        modal = Parameter.value_of('value_size_chart_modal', 'yes').lower().strip() == 'yes'
        return render(request, 'lms/sz-chart-modal.html' if modal else 'lms/sz-chart-page.html', {
            'page_title': title,
            'page_content': 'size-chart-page',
            'text': f"""#{title}\n\n#####Как выбрать одежду своего размера\n
Европейский<br/>размер | Российский<br/>размер | Рост | Обхват груди | Обхват талии | Обхват бедер
---------------------- | ----------------- | ---- | ------------ | ------------ | ------------
ХS                     | 42                | 170  | 82-85        | 60-63        | 90-93
S                      | 44                | 170  | 86-89        | 64-67        | 94-97
М                      | 46                | 170  | 90-93        | 68-71        | 98-101
L                      | 48                | 170  | 94-97        | 72-75        | 102-105
XL                     | 50                | 170  | 98-101       | 76-80        | 106-109"""})


class SCartView(View):
    @staticmethod
    @with_actual_scart_records_and_price
    def get(request, scart, *_, **__):
        return render(request, 'lms/scart.html', scart)


class FavoritesView(View):
    @staticmethod
    def get(request, *_, **__):
        return render(request, 'lms/favorites.html', {
            'products': Product.published.filter(pk__in=CustomerInfo(request).favorites),
        })


class C6tFormView(View):
    @staticmethod
    def get(request, *_, **__):
        return render(request, 'lms/c6t-form.html', {
            'c6t_form': CheckoutForm(),
        })


class C6tScartView(View):
    @staticmethod
    @with_actual_scart_records_and_price
    def get(request, scart, *_, **__):
        return render(request, 'lms/c6t-scart.html', scart)


class C6tInfoView(View):
    @staticmethod
    @with_actual_scart_records_and_price
    def get(request, kind, data, scart, *_, **__):
        match kind:
            case 'delivery':
                dv_cost = decimal.Decimal(459.70 if data == "sd" else 512.00)  # TODO !!!
                dv_days = decimal.Decimal(3 if data == "sd" else 5)  # TODO !!!
                return render(request, 'lms/c6t-d6y.html', {
                    "cost":  floatformat(dv_cost, 2),
                    "days": floatformat(dv_days),
                })
            case 'cities':
                return render(request, 'lms/c6t-city-list.html', {
                    "cities": ["СДЭК-Москва", "СДЭК-Донецк", "СДЭК-Луганск"] if data == 'sd' else ["ПР-Москва", "ПР-Донецк", "ПР-Луганск"],
                })
            case 'summary':
                dv_cost = decimal.Decimal(719.50 if data == 'sd' else 820.10)  # TODO !!!
                city = request.GET.get('city')
                return render(request, 'lms/c6t-summary.html', {
                    "items": {
                        "Сумма": f'{floatformat(scart["price"], 2)} {Parameter.value_of("label_currency")}',
                        "Доставка": f'{"СДЭК" if data == "sd" else "Почта России"}, {floatformat(dv_cost, 2)} {Parameter.value_of("label_currency")}',
                        "Назначение": f'{city if city else "г. Москва, Россия"}',
                        "Итоговая сумма": f'{floatformat(scart["price"] + dv_cost, 2)} {Parameter.value_of("label_currency")}',
                    }
                })
            case _: return render(request, 'lms/c6t-summary.html', {
                "items": {
                    "Ошибка": "Запрошен неизвестный тип данных"
                }
            })
