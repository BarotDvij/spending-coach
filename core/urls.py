from django.urls import path, include
from core.views_summary import get_monthly_spend_summary
from rest_framework import routers
from .views import TransactionViewSet, BudgetViewSet, InsightViewSet

router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'insights', InsightViewSet)

urlpatterns = [
    path("summary/", get_monthly_spend_summary, name="summary"),  # ✅ fixed name here
]

urlpatterns += router.urls

