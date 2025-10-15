from django.urls import path
from rest_framework import routers
from .views import TransactionViewSet, BudgetViewSet, InsightViewSet
from core.views_summary import get_monthly_spend_summary

router = routers.DefaultRouter()
router.register(r"transactions", TransactionViewSet)
router.register(r"budgets", BudgetViewSet)
router.register(r"insights", InsightViewSet)

urlpatterns = [
    path("summary/", get_monthly_spend_summary, name="summary"),
]
urlpatterns += router.urls
