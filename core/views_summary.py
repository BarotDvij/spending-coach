from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date
from django.contrib.auth.models import User
from core.models import Budget, Insight, Subscription
from core.serializers import BudgetSerializer, InsightSerializer, SubscriptionSerializer
from core.services.summary import get_monthly_summary

@api_view(["GET"])
def get_monthly_spend_summary(request):
    user_id = request.query_params.get("user", 1)
    y = int(request.query_params.get("year", date.today().year))
    m = int(request.query_params.get("month", date.today().month))

    user = User.objects.get(id=user_id)
    summary = get_monthly_summary(user, y, m)
    budgets = BudgetSerializer(Budget.objects.filter(user=user, year=y, month=m), many=True).data
    insights = InsightSerializer(Insight.objects.filter(user=user, year=y, month=m).order_by("-created_at")[:20], many=True).data
    subs = SubscriptionSerializer(Subscription.objects.filter(user=user).order_by("-confidence")[:10], many=True).data

    return Response({
        "summary": summary,
        "budgets": budgets,
        "insights": insights,
        "subscriptions": subs,
    })
