from django.http import JsonResponse
from rest_framework import viewsets, filters
from .models import Transaction, Budget, Insight
from .serializers import TransactionSerializer, BudgetSerializer, InsightSerializer

def hello_world(request):
    return JsonResponse({"message": "Hello, Spending Coach!"})

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by("-date", "-id")
    serializer_class = TransactionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["description", "category"]
    ordering_fields = ["date", "amount", "created_at"]

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

class InsightViewSet(viewsets.ModelViewSet):
    queryset = Insight.objects.all()
    serializer_class = InsightSerializer