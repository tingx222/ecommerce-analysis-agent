from decimal import Decimal

from sample_orders import ORDERS


def calculate_sales_summary():
    paid_order_count = 0
    total_sales = Decimal("0.00")

    for order in ORDERS:
        if order["status"] == "PAID":
            paid_order_count += 1
            total_sales += Decimal(order["amount"])

    return {
        "paid_order_count": paid_order_count,
        "total_sales": str(total_sales),
        "currency": "CNY",
        "data_source": "sample",
    }