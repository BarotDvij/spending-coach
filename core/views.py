from rest_framework import viewsets, filters
from .models import Transaction, Budget, Insight
from .serializers import TransactionSerializer, BudgetSerializer, InsightSerializer
from .tasks import compute_insights, process_transaction_rewards  # ← ADD THIS IMPORT
from datetime import date

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by("-date", "-id")
    serializer_class = TransactionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["description", "category"]
    ordering_fields = ["date", "amount", "created_at"]

    def perform_create(self, serializer):
        obj = serializer.save()
        d = obj.date or date.today()
        
        # Trigger insights calculation
        compute_insights.delay(obj.user_id, d.year, d.month)
        
        # NEW: Trigger instant reward badges
        process_transaction_rewards.delay(obj.user_id, obj.id)

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all().order_by("-year", "-month", "category")
    serializer_class = BudgetSerializer

class InsightViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Insight.objects.all().order_by("-created_at")
    serializer_class = InsightSerializer