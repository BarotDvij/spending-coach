# core/logic/reward_engine.py

from datetime import date, timedelta
from django.db.models import Sum
from core.models import Transaction, Budget
from core.models import RewardsLedger, Badge, Streak

def calculate_user_rewards(user):
    today = date.today()
    year, month = today.year, today.month

    # Get total budget for this month
    total_budget = (
        Budget.objects.filter(user=user, year=year, month=month)
        .aggregate(Sum("amount"))["amount__sum"] or 0
    )

    # Get actual spend for this month
    total_spent = (
        Transaction.objects.filter(user=user, date__year=year, date__month=month)
        .aggregate(Sum("amount"))["amount__sum"] or 0
    )

    if total_budget == 0:
        return 0

    # Calculate performance ratio
    percent_used = (total_spent / total_budget) * 100
    percent_below = max(0, 100 - percent_used)
    percent_above = max(0, percent_used - 100)

    # --- Weekly / Monthly Point Logic ---
    points = 0

    # Points gained or lost based on performance
    if percent_below > 0:
        points += int((percent_below // 10) * 25)
    elif percent_above > 0:
        points -= int((percent_above // 10) * 25)

    # Monthly badges
    if percent_below >= 10:
        level = int(percent_below // 10)
        badge_points = level * 35
        badge_name = [
            "Goal Getter", "Smart Saver", "Money Magician", "Cashflow Commander"
        ][min(level - 1, 3)]
        Badge.objects.update_or_create(
            user=user,
            month=month,
            year=year,
            defaults={"name": badge_name, "points": badge_points},
        )
        points += badge_points

    # --- Streaks ---
    last_two_weeks = today - timedelta(days=14)
    recent_spending = (
        Transaction.objects.filter(user=user, date__gte=last_two_weeks)
        .aggregate(Sum("amount"))["amount__sum"] or 0
    )
    recent_budget = (
        Budget.objects.filter(user=user, year=year, month=month)
        .aggregate(Sum("amount"))["amount__sum"] or 0
    )

    if recent_budget > 0 and recent_spending <= recent_budget:
        streak, created = Streak.objects.get_or_create(user=user)
        streak.count += 1
        streak.points += 20
        streak.save()
        points += 20

    # --- Rewards Ledger ---
    RewardsLedger.objects.create(
        user=user, month=month, year=year, points_earned=points, total_spent=total_spent
    )

    return points
