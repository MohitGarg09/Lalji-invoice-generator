from io import BytesIO
from typing import Iterable
from openpyxl import Workbook, load_workbook
from django.db import transaction
from .models import Sweet, Invoice, InvoiceItem


SWEETS_HEADERS = ["name", "sweet_type", "price_per_kg", "price_per_unit"]


def export_sweets_to_excel(sweets: Iterable[Sweet]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Sweets"
    ws.append(SWEETS_HEADERS)
    for s in sweets:
        ws.append([
            s.name,
            s.sweet_type,
            float(s.price_per_kg) if s.price_per_kg is not None else None,
            float(s.price_per_unit) if s.price_per_unit is not None else None,
        ])
    bio = BytesIO()
    wb.save(bio)
    return bio.getvalue()


@transaction.atomic
def import_sweets_from_excel(excel_bytes: bytes) -> int:
    wb = load_workbook(filename=BytesIO(excel_bytes))
    ws = wb.active
    headers = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))[0:len(SWEETS_HEADERS)]]
    if [h.lower() if isinstance(h, str) else h for h in headers] != SWEETS_HEADERS:
        raise ValueError("Invalid header row for sweets import. Expected: " + ",".join(SWEETS_HEADERS))
    created_or_updated = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if all(v is None for v in row):
            continue
        name, sweet_type, price_per_kg, price_per_unit = row[:4]
        obj, _created = Sweet.objects.update_or_create(
            name=str(name).strip(),
            defaults={
                'sweet_type': str(sweet_type).strip(),
                'price_per_kg': price_per_kg or None,
                'price_per_unit': price_per_unit or None,
            }
        )
        created_or_updated += 1
    return created_or_updated


def export_invoice_to_excel(invoice: Invoice) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = f"Invoice_{invoice.id}"
    # Header area
    ws.append(["Invoice ID", invoice.id])
    ws.append(["Customer", invoice.customer_name or "-"])
    ws.append(["Date", invoice.created_at.strftime("%Y-%m-%d %H:%M")])
    ws.append(["Discount %", float(invoice.discount_percent)])
    ws.append(["Subtotal", float(invoice.subtotal)])
    ws.append(["Total", float(invoice.total)])
    ws.append([])

    # Items
    ws.append(["Sweet", "Type", "Gross g", "Tray g", "Net g", "Count", "Amount"]) 
    for item in invoice.items.select_related("sweet"):
        ws.append([
            item.sweet.name,
            item.sweet.sweet_type,
            float(item.gross_weight_g) if item.gross_weight_g is not None else None,
            float(item.tray_weight_g) if item.tray_weight_g is not None else None,
            float(item.net_weight_g) if item.net_weight_g is not None else None,
            item.count,
            float(item.total_amount),
        ])

    bio = BytesIO()
    wb.save(bio)
    return bio.getvalue()


def export_invoices_to_excel(invoices: Iterable[Invoice]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoices"
    ws.append(["Invoice ID", "Customer", "Created At", "Discount %", "Subtotal", "Total"]) 
    for inv in invoices:
        ws.append([
            inv.id,
            inv.customer_name or "-",
            inv.created_at.strftime("%Y-%m-%d %H:%M"),
            float(inv.discount_percent),
            float(inv.subtotal),
            float(inv.total),
        ])

    bio = BytesIO()
    wb.save(bio)
    return bio.getvalue()


