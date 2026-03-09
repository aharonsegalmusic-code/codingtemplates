from fastapi import APIRouter

from .dal import top_customers, customers_without_orders, zero_credit_active_customers

router = APIRouter()


@router.get("/analytics/top-customers")
def top_customers_route():
    rows = top_customers()
    return [{"customerNumber": r[0], "customerName": r[1], "ordersCount": int(r[2])} for r in rows]


@router.get("/analytics/customers-without-orders")
def customers_without_orders_route():
    rows = customers_without_orders()
    return [{"customerNumber": r[0], "customerName": r[1]} for r in rows]


@router.get("/analytics/zero-credit-active-customers")
def zero_credit_active_customers_route():
    rows = zero_credit_active_customers()
    return [
        {
            "customerNumber": r[0],
            "customerName": r[1],
            "creditLimit": float(r[2]),
            "ordersCount": int(r[3]),
        }
        for r in rows
    ]