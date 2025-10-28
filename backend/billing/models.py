from django.db import models


class Sweet(models.Model):
    TYPE_WEIGHT = 'weight'
    TYPE_COUNT = 'count'
    TYPE_CHOICES = [
        (TYPE_WEIGHT, 'By Weight'),
        (TYPE_COUNT, 'By Count'),
    ]

    name = models.CharField(max_length=100, unique=True)
    sweet_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100, blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # legacy
    payment_mode = models.CharField(max_length=10, choices=[('cash', 'Cash'), ('credit', 'Credit')], default='cash', null=True, blank=True)
    bill_type = models.CharField(max_length=10, choices=[('GST', 'GST'), ('Non-GST', 'Non-GST')], default='GST', null=True, blank=True)
    dm_no = models.CharField(max_length=100, blank=True, null=True)
    @property
    def subtotal(self):
        return sum(item.total_amount for item in self.items.all())

    @property
    def total(self):
        try:
            pct = float(self.discount_percent or 0)
        except Exception:
            pct = 0
        pct = min(max(pct, 0), 100)
        discounted = self.subtotal * (1 - (pct / 100))
        return max(discounted, 0)

    def __str__(self):
        return f"Invoice #{self.id or '—'} ({self.customer_name})"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    sweet = models.ForeignKey(Sweet, on_delete=models.PROTECT)

    # for weight-based sweets (in kg now)
    gross_weight_kg = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    tray_weight_kg = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    # for count-based sweets
    count = models.PositiveIntegerField(null=True, blank=True)

    # Optional per-item unit price override (per kg for weight, per piece for count)
    unit_price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def net_weight_kg(self):
        """Return net weight in kg."""
        if self.gross_weight_kg is not None and self.tray_weight_kg is not None:
            net = self.gross_weight_kg - self.tray_weight_kg
            return max(net, 0)
        return None

    @property
    def total_amount(self):
        """Compute total based on kg for weight type and count for count type."""
        if self.sweet.sweet_type == Sweet.TYPE_WEIGHT:
            if self.net_weight_kg is None:
                return 0
            price = self.unit_price_override if self.unit_price_override is not None else self.sweet.price_per_kg
            return float(self.net_weight_kg) * float(price or 0)
        else:
            if not self.count:
                return 0
            price = self.unit_price_override if self.unit_price_override is not None else self.sweet.price_per_unit
            return float(self.count) * float(price or 0)

    def __str__(self):
        return f"{self.sweet.name} ({self.invoice_id})"
