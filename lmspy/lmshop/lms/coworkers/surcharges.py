from decimal import Decimal


def d6y_cost_with_surcharges(d6y_svc: any, d6y_cost: Decimal, goods_cost: Decimal):
    cost = eval(d6y_svc.setting('delivery-with-surcharges', 'delivery'), {}, {
        'delivery': float(d6y_cost),
        'goods': float(goods_cost)
    })
    return Decimal(round(cost, 2))
