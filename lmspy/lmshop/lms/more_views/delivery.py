from django.shortcuts import render
from django.views import View
from lms.models import Parameter


class DeliveryView(View):
    @staticmethod
    def get(request, *_, **__):
        return render(request, 'lms/delivery.html', {
            'page_title': Parameter.value_of("title_delivery", "Доставка и оплата"),
            'page_content': 'delivery',
            'text': f"""#ДОСТАВКА\n\nУважаемые покупатели, получить свой заказ вы можете транспортной компанией СДЭК или Почта России по всей России, 
            а так же DHL в любую точку мира.\n\n##Доставка по России\n\nСрок формирования и отправки заказа 2-4 рабочих дня после оплаты. Стоимость и сроки
            доставки рассчитываются индивидуально для каждого города, с тарифами и сроками доставки можно ознакомиться на сайте при оформлении заказа. 
            \n\nДоставка внутри страны осуществляется:\n\n1. Транспортной компанией СДЭК (до двери или до пункта самовывоза) во все города России от 2 
            до 10 рабочих дней.\n\n1. Доставка Почтой России до любого удобного вам отделения.\n\n#ОПЛАТА\n\nПокупки можно оплатить с помощью безналичного 
            расчёта при оформлении заказа.\n\nК оплате принимаются карты платёжных систем Visa, MasterCard и Мир. Чтобы оплатить заказ онлайн, выберите 
            соответствующий пункт. Вам будет предложено проверить введённые вами личные данные, адрес доставки и выбранные товары, а затем подтвердить их, 
            нажав кнопку «Оформить заказ». Откроется страница, на которой необходимо будет ввести данные карты, проверить их и нажать кнопку «Оплатить».
            \n\n#ВОЗВРАТ\n\n***Покупатели, обратите внимание!***\n\nВозврат осуществляется при наличии заполненного заявления (скачать заявление можно по ссылке 
            [«Заявление»]({Parameter.value_of("value_link_application_form")}))\n\nОбмену и возврату подлежат изделия, если их товарный вид не нарушен, нет следов носки, и загрязнений, а также сохранены товарные 
            этикетки.\n\nВозврат осуществляется за счет Покупателя.\n\nВ каждый заказ необходимо вложить бланк с заявлением на возврат.
            \n\n##ВОЗВРАТ ИНТЕРНЕТ-ЗАКАЗА В ОНЛАЙН-БУТИК LUBMI\n\nУ Покупателя есть 7 дней после получения интернет-заказа для возврата товара в онлайн-магазин. В 
            соответствии Постановлении Правительства РФ от 31 декабря 2020 г. N 2463 п.22 "_Об утверждении Правил продажи товаров по договору розничной купли-продажи, 
            перечня товаров длительного пользования, на которые не распространяется требование потребителя о безвозмездном предоставлении ему товара, обладающего 
            этими же основными потребительскими свойствами, на период ремонта или замены такого товара, и перечня непродовольственных товаров надлежащего 
            качества, не подлежащих обмену, а также о внесении изменений в некоторые акты Правительства Российской Федерации_"\n\nДля возврата необходимо вещи 
            упаковать в пакет и коробку, и приложить заявление на возврат.\n\nВозврат денежных средств при безналичном расчете осуществляется непосредственно на
            счёт, с которого происходила оплата.\n\nПосле одобрения возврата, покупателю будут перечислены денежные средства на карту или банковский счет в 
            течении 10ти банковских дней, для этого необходимо заполнить полные реквизиты для перевода денежных средств в заявлении на возврат. В случае проблем 
            с прохождением платежа с покупателем связывается сотрудник онлайн-бутика для уточнения реквизитов. Обращаем внимание покупателей, возврат денежных 
            средств зависит от скорости обработки операции вашим Банком и может достигать 30 банковских дней.\n\n##ОТПРАВКА ВОЗВРАТА\n\nОсуществить возврат 
            можно в течении 7 дней после получения товара. Возврат товара надлежащего качества возможен лишь в том случае, если сохранены его товарный вид, 
            этикетки, ярлыки, и потребительские свойства.\n\nК товару на возврат приложите заявление на возврат. Упакуйте все вещи для возврата в пакет и 
            коробку, в которой был получен данный заказ. Отправьте на номер {Parameter.value_of("value_return_phone")} следующую информацию: фотографию 
            заполненного заявления и трек номер отправления. Отправьте посылку курьерской компанией СДЭК или Почтой России.\n\n###Отправка через ПВЗ СДЭК
            \n\n    {Parameter.value_of("value_return_address_sdek")}\n    Отправлять на имя Мишанковой Любови Алексеевны\n    Контактный телефон: {Parameter.value_of("value_return_phone")}
            \n\n###Отправка Почтой России\n\n    {Parameter.value_of("value_return_address_pr")}\n    На имя Мишанковой Л.А.\n    Контактный телефон: {Parameter.value_of("value_return_phone")}
            \n\nПосле получения и проверки возврата, покупателю будут перечислены денежные средства на карту или банковский счет в срок до 10ти рабочих дней, 
            для этого необходимо заполнить полные реквизиты для перевода денежных средств в заявлении на возврат. В случае проблем с прохождением платежа с 
            вами свяжется сотрудник онлайн-бутика для уточнения реквизитов. Обращаем ваше внимание, что возврат денежных средств зависит от скорости обработки 
            операции вашим банком и может достигать 30 банковских дней.\n\nВозврат денежных средств осуществляется за вычетом суммы доставки.\n\nВ случае 
            нарушений вышеуказанных условий оформления возврата или обмена товара (отсутствие заполненного заявления; заявление заполнено не полностью или с ошибками;
            отсутствуют необходимые документы) магазин не дает гарантий на поступление товара на условиях возврата или обмена в магазин. В связи с этим магазин 
            не гарантирует оплату данного товара.""",
        })
