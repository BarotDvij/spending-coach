from core.models import Transaction
from django.db.models import Sum
from datetime import date

def get_monthly_summary(user, year=None, month=None):
    today = date.today()
    year = year or today.year
    month = month or today.month

    data = {
        Transaction.objects
        .filter(user=user, date__year=year, date__month=month)
        .values("category")
        .annotate(total=Sum("amount"))
    }

    total_spent = sum(item["total"] for item in data)
    return {"year": year, "month": month, "total_spent": total_spent, "by_category": list(data), "total": total_spent}