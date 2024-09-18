from decimal import Decimal


# def d6y_cost_with_surcharges(d6y_svc: any, d6y_cost: Decimal, goods_cost: Decimal):
#     cost = eval(d6y_svc.setting('delivery-with-surcharges', 'delivery'), {}, {
#         'delivery': float(d6y_cost),
#         'goods': float(goods_cost)
#     })
#     return Decimal(round(cost, 2))

def d6y_cost_with_surcharges(d6y_svc: any, d6y_cost: Decimal, goods_cost: Decimal):
    goods_factor = Decimal(d6y_svc.setting("surcharge-goods-percents", "0")) / Decimal(100)
    agent_factor = Decimal(1) + Decimal(d6y_svc.setting("surcharge-agent-percents", "0")) / Decimal(100)
    add_sur = Decimal(d6y_svc.setting("surcharge-additional", "0"))
    return round((d6y_cost + goods_cost * goods_factor) * agent_factor + add_sur, 2)