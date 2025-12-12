from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ("food", "Food"),
    ("transport", "Transport"),
    ("entertainment", "Entertainment"),
    ("shopping", "Shopping"),
    ("rent", "Rent"),
    ("other", "Other"),
]

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES, default="misc")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["user", "category", "date"]),
        ]

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.CharField(max_length=100, default="misc")   # ✅ same fix
    month = models.IntegerField()
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("user", "category", "month", "year")
        indexes = [models.Index(fields=["user", "year", "month", "category"])]

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant = models.CharField(max_length=255)
    avg_amount = models.DecimalField(max_digits=10, decimal_places=2)
    last_seen = models.DateField()
    next_estimated_date = models.DateField(null=True, blank=True)
    confidence = models.FloatField(default=0.0)
    occurrences = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "merchant")
        indexes = [models.Index(fields=["user", "merchant"])]

INSIGHT_TYPES = [
    ("budget_threshold", "Budget Threshold"),
    ("subscription_detected", "Subscription Detected"),
    ("anomaly", "Anomaly"),
]

SEVERITY = [
    ("info", "Info"),
    ("warning", "Warning"),
    ("alert", "Alert"),
]

class Insight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="insights")
    year = models.IntegerField()
    month = models.IntegerField()
    type = models.CharField(max_length=64, choices=INSIGHT_TYPES)
    severity = models.CharField(max_length=16, choices=SEVERITY, default="info")
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

class RewardsLedger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    points_earned = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    year = models.IntegerField()
    month = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Streak(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["user", "year", "month", "type", "created_at"])]

