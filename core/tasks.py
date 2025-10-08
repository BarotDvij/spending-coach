from celery import shared_task
from django.db.models import Sum
from .models import Transaction, Budget, Insight
from core.services.summary import get_monthly_summary
from core.services.recommend import generate_insights
from django.contrib.auth.models import User

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

@shared_task
def compute_insights(user_id, year, month):
    """Celery task to generate and save insights for a user."""
    user = User.objects.get(id=user_id)
    budgets = Budget.objects.filter(user=user, year=year, month=month)
    summary = get_monthly_summary(user, year, month)
    insights = generate_insights(summary, budgets)

    for i in insights:
        Insight.objects.create(
            user=user,
            year=year,
            month=month,
            type=i["type"],
            payload=i["payload"],
            severity=i["severity"]
        )

    return f"{len(insights)} insights created for {user.username}"