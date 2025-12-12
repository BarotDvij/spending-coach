from celery import shared_task
from django.contrib.auth.models import User
from datetime import date
from core.services.summary import get_monthly_summary
from core.services.subscriptions import detect_subscriptions_for_month
from core.services.insights import generate_budget_insights
from core.logic.reward_engine import calculate_user_rewards

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

@shared_task
def run_monthly_rewards():
    for user in User.objects.all():
        points = calculate_user_rewards(user)
        print(f"Rewards calculated for user {user.username}: {points}")
