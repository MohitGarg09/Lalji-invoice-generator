from django.contrib import admin
from .models import Sweet, Invoice, InvoiceItem


@admin.register(Sweet)
class SweetAdmin(admin.ModelAdmin):
	list_display = ("name", "sweet_type", "price_per_kg", "price_per_unit")
	list_filter = ("sweet_type",)
	search_fields = ("name",)


class InvoiceItemInline(admin.TabularInline):
	model = InvoiceItem
	extra = 0
	fields = ("sweet", "gross_weight_g", "tray_weight_g", "count", "unit_price_override")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	list_display = ("id", "customer_name", "created_at", "discount_amount")
	date_hierarchy = "created_at"
	inlines = [InvoiceItemInline]
