from decimal import Decimal


def d6y_cost_with_surcharges(d6y_svc: any, d6y_cost: Decimal, goods_cost: Decimal):
    goods_factor = Decimal(d6y_svc.setting("surcharge-goods-percents", "0")) / Decimal(100)
    d6y_factor = Decimal(1) + Decimal(d6y_svc.setting("surcharge-delivery-percents", "0")) / Decimal(100)
    add_sur = Decimal(d6y_svc.setting("surcharge-additional", "0"))
    return round(d6y_cost * d6y_factor + goods_cost * goods_factor + add_sur, 2)
