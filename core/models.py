from django.db import models

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
