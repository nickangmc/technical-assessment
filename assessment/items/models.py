from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):

    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        "items.Category",
        on_delete=models.PROTECT,
        related_name="items",
    )

    # Note: Follows the best-practiced format for a currency field
    # Reference: https://stackoverflow.com/questions/224462/storing-money-in-a-decimal-column-what-precision-and-scale/
    price = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        validators=[MinValueValidator(Decimal(1))],
    )

    # Auto-assigned fields
    created_dt = models.DateTimeField(auto_now_add=True)
    last_updated_dt = models.DateTimeField(auto_now=True)


class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)

    # Auto-assigned fields
    created_dt = models.DateTimeField(auto_now_add=True)
    last_updated_dt = models.DateTimeField(auto_now=True)
