from datetime import date
from decimal import Decimal
from collections import defaultdict
from django.db.models import Sum
from core.models import Transaction

def get_monthly_summary(user, year=None, month=None):
    today = date.today()
    year = year or today.year
    month = month or today.month

    qs = (Transaction.objects
          .filter(user=user, date__year=year, date__month=month)
          .values("category")
          .annotate(total=Sum("amount")))

    by_category = [{"category": row["category"], "total": float(row["total"] or Decimal("0"))}
                   for row in qs]
    total_spent = float(sum(row["total"] for row in by_category))
    return {
        "year": year,
        "month": month,
        "by_category": by_category,
        "total_spent": total_spent,
    }
