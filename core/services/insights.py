from core.models import Budget, Insight, Transaction
from datetime import date
from decimal import Decimal
from django.db.models import Sum

THRESHOLDS = [(0.8, "alert"), (0.5, "warning")]  # 80% alert, 50% warning

def generate_budget_insights(user, year, month):
    budgets = Budget.objects.filter(user=user, year=year, month=month)
    tx = (Transaction.objects
          .filter(user=user, date__year=year, date__month=month)
          .values("category")
          .annotate(total=Sum("amount")))
    spent = {row["category"]: Decimal(str(row["total"])) for row in tx}

    created = 0
    for b in budgets:
        used = spent.get(b.category, Decimal("0"))
        if b.amount and b.amount > 0:
            pct = float((used / b.amount))
            for thr, sev in THRESHOLDS:
                if pct >= thr:
                    Insight.objects.create(
                        user=user,
                        year=year,
                        month=month,
                        type="budget_threshold",
                        severity=sev,
                        payload={
                            "category": b.category,
                            "spent": float(used),
                            "budget": float(b.amount),
                            "percent_used": round(pct*100, 1),
                            "threshold": int(thr*100),
                        }
                    )
                    created += 1
                    break
    return created
