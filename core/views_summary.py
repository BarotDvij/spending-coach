from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from django.contrib.auth.models import User

from core.services.summary import get_monthly_summary
from core.models import Budget, Insight

@api_view(['GET'])
@permission_classes([])
def get_monthly_spend_summary(request):
    user_id = request.query_params.get("user", 1)
    year = int(request.query_params.get("year", date.today().year))
    month = int(request.query_params.get("month", date.today().month))

    user = User.objects.get(id=user_id)
    summary = get_monthly_summary(user, year, month)
    budgets = Budget.objects.filter(user=user, year=year, month=month)
    insights = Insight.objects.filter(user=user, year=year, month=month)
    return Response({
        "summary": summary,
        "budgets": budgets,
        "insights": insights
    }, status=status.HTTP_200_OK)