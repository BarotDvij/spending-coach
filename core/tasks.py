from celery import shared_task
from django.contrib.auth.models import User
from datetime import date
from core.services.summary import get_monthly_summary
from core.services.subscriptions import detect_subscriptions_for_month
from core.services.insights import generate_budget_insights

@shared_task
def compute_insights(user_id, year, month):
    user = User.objects.get(id=user_id)
    # 1) detect subscriptions (idempotent upsert)
    detect_subscriptions_for_month(user, year, month)
    # 2) generate budget threshold insights (append-only)
    created = generate_budget_insights(user, year, month)
    # Optionally return a compact result
    summary = get_monthly_summary(user, year, month)
    return {"insights_created": created, "summary": summary}

@shared_task
def recompute_current_month(user_id):
    today = date.today()
    return compute_insights.delay(user_id, today.year, today.month)
