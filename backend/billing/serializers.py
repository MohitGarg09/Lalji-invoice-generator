from rest_framework import serializers
from .models import Sweet, Invoice, InvoiceItem


class SweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sweet
        fields = ['id', 'name', 'sweet_type', 'price_per_kg', 'price_per_unit']


class InvoiceItemSerializer(serializers.ModelSerializer):
    net_weight_kg = serializers.DecimalField(max_digits=10, decimal_places=3, read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    unit_price_override = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)

    class Meta:
        model = InvoiceItem
        fields = [
            'id', 'sweet', 'gross_weight_kg', 'tray_weight_kg', 'net_weight_kg', 'count', 'unit_price_override', 'total_amount'
        ]


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'created_at', 'customer_name', 'discount_percent', 'subtotal', 'dm_no', 'payment_mode', 'bill_type', 'total', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        invoice = Invoice.objects.create(**validated_data)
        for item in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item)
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                InvoiceItem.objects.create(invoice=instance, **item)
        return instance


