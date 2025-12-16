from celery import shared_task
from django.contrib.auth.models import User
from datetime import date
from core.services.summary import get_monthly_summary
from core.services.subscriptions import detect_subscriptions_for_month
from core.services.insights import generate_budget_insights
from core.logic.reward_engine import (
    calculate_user_rewards,
    award_transaction_badges,
    reset_monthly_rewards
)

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
def process_transaction_rewards(user_id, transaction_id):
    """
    Called immediately after a transaction is created.
    Awards real-time badges (e.g., logging streaks, first transaction).
    """
    user = User.objects.get(id=user_id)
    badges_earned = award_transaction_badges(user, transaction_id)
    return {"user": user.username, "badges": badges_earned}

@shared_task
def run_monthly_rewards():
    """
    Scheduled task (runs on the 1st of each month via Celery Beat).
    Calculates points, awards badges, and resets streaks.
    """
    for user in User.objects.all():
        # Calculate points for last month
        points = calculate_user_rewards(user)
        
        # Award monthly badges (e.g., "Budget Master", "Under Budget 3 Months")
        reset_monthly_rewards(user, points)
        
        print(f"✅ Monthly rewards processed for {user.username}: {points} points")
    
    return {"status": "completed", "users_processed": User.objects.count()}