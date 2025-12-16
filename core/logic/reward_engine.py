from datetime import date, timedelta
from django.db.models import Sum, Count
from core.models import Transaction, Budget, RewardsLedger, Badge, Streak

def calculate_user_rewards(user):
    """
    Calculates monthly points based on budget performance.
    Called by run_monthly_rewards task on the 1st of each month.
    """
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

    # --- Streaks (FIXED) ---
    last_two_weeks = today - timedelta(days=14)
    recent_spending = (
        Transaction.objects.filter(user=user, date__gte=last_two_weeks)
        .aggregate(Sum("amount"))["amount__sum"] or 0
    )
    
    # FIX: Pro-rate budget for 2-week comparison
    # Instead of comparing 2-week spending to full month budget
    days_in_month = 30  # Approximation (could use calendar.monthrange for precision)
    recent_budget_proportion = (total_budget / days_in_month) * 14

    if recent_budget_proportion > 0 and recent_spending <= recent_budget_proportion:
        streak, created = Streak.objects.get_or_create(user=user)
        streak.count += 1
        streak.points += 20
        streak.save()
        points += 20
    else:
        # Reset streak if user went over budget
        try:
            streak = Streak.objects.get(user=user)
            streak.count = 0
            streak.save()
        except Streak.DoesNotExist:
            pass

    # --- Rewards Ledger ---
    RewardsLedger.objects.create(
        user=user, 
        month=month, 
        year=year, 
        points_earned=points, 
        total_spent=total_spent
    )

    return points


def award_transaction_badges(user, transaction_id):
    """
    Awards instant badges when a transaction is logged.
    Called by process_transaction_rewards task after each transaction.
    
    Returns: List of badge names earned
    """
    from django.db import connection
    
    # Force database to commit any pending transactions
    connection.commit()
    
    badges_earned = []
    
    # IMPORTANT: Use .count() on a fresh query to avoid caching
    transaction_count = Transaction.objects.filter(user=user).count()
    
    # Check if this is the user's first transaction ever
    if transaction_count == 1:
        Badge.objects.create(
            user=user,
            name="First Step",
            badge_type="milestone",
            points=10,
            month=date.today().month,
            year=date.today().year
        )
        badges_earned.append("First Step")
    
    # Check logging streak (consecutive days with transactions)
    streak_days = calculate_logging_streak(user)
    
    # Award badges at milestone days
    if streak_days in [5, 10, 30, 60, 100]:
        Badge.objects.create(
            user=user,
            name=f"{streak_days}-Day Streak",
            badge_type="streak",
            points=streak_days // 5 * 10,
            month=date.today().month,
            year=date.today().year
        )
        badges_earned.append(f"{streak_days}-Day Streak")
    
    # Milestone transaction counts
    if transaction_count in [10, 50, 100, 500]:
        Badge.objects.create(
            user=user,
            name=f"{transaction_count} Transactions",
            badge_type="milestone",
            points=transaction_count // 10,
            month=date.today().month,
            year=date.today().year
        )
        badges_earned.append(f"{transaction_count} Transactions")
    
    return badges_earned


def calculate_logging_streak(user):
    """
    Calculates how many consecutive days the user has logged transactions.
    Returns: int (number of consecutive days)
    """
    today = date.today()
    streak = 0
    current_day = today
    
    # Go backwards day by day until we find a day with no transactions
    while True:
        has_transaction = Transaction.objects.filter(
            user=user,
            date=current_day
        ).exists()
        
        if has_transaction:
            streak += 1
            current_day -= timedelta(days=1)
        else:
            break
        
        # Safety limit to prevent infinite loops
        if streak > 365:
            break
    
    return streak


def reset_monthly_rewards(user, points):
    """
    Called on the 1st of each month to finalize rewards.
    Saves points to user profile and resets monthly counters.
    
    Args:
        user: User object
        points: Points earned this month (from calculate_user_rewards)
    """
    # Get or create user profile (you may need to adjust this based on your model)
    # Option 1: If you have a UserProfile model
    # profile, created = UserProfile.objects.get_or_create(user=user)
    # profile.total_points += points
    # profile.save()
    
    # Option 2: If you're storing points directly on User model
    # user.total_points = (user.total_points or 0) + points
    # user.save()
    
    # For now, we'll just log it (you can implement profile logic later)
    print(f"Would save {points} points to {user.username}'s profile")
    
    # Award "consistent performer" badge if user stayed under budget
    # for 3+ months in a row
    recent_ledger = RewardsLedger.objects.filter(
        user=user
    ).order_by('-year', '-month')[:3]
    
    if len(recent_ledger) == 3 and all(entry.points_earned > 0 for entry in recent_ledger):
        Badge.objects.create(
            user=user,
            name="Consistent Performer",
            badge_type="achievement",
            points=100,
            month=date.today().month,
            year=date.today().year
        )
    
    # Note: We're NOT resetting the Streak model here because it tracks
    # ongoing 2-week periods, not monthly resets. It resets automatically
    # in calculate_user_rewards when user goes over budget.