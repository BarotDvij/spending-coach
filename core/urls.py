from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import hello_world, TransactionViewSet  # <-- import the function directly

router = DefaultRouter()
router.register(r"api/transactions", TransactionViewSet, basename="transactions")

urlpatterns = [
    path("hello/", hello_world),   # <-- use the imported name, not views.hello_world
    path("", include(router.urls)),
]