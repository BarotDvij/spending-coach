from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ("food", "Food"),
        ("transport", "Transport"),
        ("rent", "Rent"),
        ("shopping", "Shopping"),
        ("other", "Other"),
    ]

    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # positive = expense
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default="other")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} • {self.description} • {self.amount}"
    
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"{self.user.username} - {self.category} - ({self.month}/{self.year})"
    
class Insight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    type = models.CharField(max_length=100)
    payload = models.JSONField()
    severity = models.CharField(max_length=20, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")])
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - {self.month}/{self.year}"
