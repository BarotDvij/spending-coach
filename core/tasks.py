from celery import shared_task
from django.db.models import Sum
from .models import Transaction

@shared_task
def ping(name="world"):
    return f"hello {name}"

@shared_task
def monthly_spend_summary(year: int, month: int):
    qs = Transaction.objects.filter(date__year=year, date__month=month)
    total = qs.aggregate(total=Sum("amount"))["total"] or 0
    by_category = list(
        qs.values("category").annotate(total=Sum("amount")).order_by("-total")
    )
    return {"year": year, "month": month, "total": float(total), "by_category": by_category}