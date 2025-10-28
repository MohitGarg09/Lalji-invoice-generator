# from io import BytesIO
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import mm
# from reportlab.lib import colors
# from decimal import Decimal

# def render_invoice_pdf(invoice):
#     buffer = BytesIO()
#     c = canvas.Canvas(buffer, pagesize=A4)
#     width, height = A4

#     # --- Fonts ---
#     HEADER_FONT = ("Helvetica-Bold", 18)
#     COMPANY_FONT = ("Helvetica-Bold", 14)
#     SUBHEADER_FONT = ("Helvetica-Bold", 12)
#     ROW_FONT = ("Helvetica", 10)
#     SMALL_FONT = ("Helvetica", 9)
#     TOTAL_FONT = ("Helvetica-Bold", 11)

#     # --- Margins ---
#     left_margin = 15 * mm
#     right_margin = width - 15 * mm
#     y = height - 20 * mm

#     # --- Company Header ---
#     header_height = 22 * mm
#     c.setFillColor(colors.HexColor('#f8f9fa'))
#     c.setStrokeColor(colors.HexColor('#dee2e6'))
#     c.rect(left_margin, y - header_height, right_margin - left_margin, header_height, fill=True, stroke=True)
#     c.setFillColor(colors.HexColor('#2c3e50'))
#     c.setFont(*HEADER_FONT)
#     c.drawCentredString(width / 2, y - 25, "AGRAWAL DAIRY AND SWEETS")
#     c.setFillColor(colors.HexColor('#495057'))
#     c.setFont(*ROW_FONT)
#     c.drawCentredString(width / 2, y - 40, "Radha Kisan Plots, Infront of GMC, Akola - 444001")
#     c.drawCentredString(width / 2, y - 52, "Mobile: 9822066728")
#     y -= 25 * mm

#     # --- Invoice Info ---
#     c.setFont(*SUBHEADER_FONT)
#     c.drawString(left_margin, y - 10, "INVOICE")
#     info_box_width = 70 * mm
#     info_box_height = 15 * mm
#     c.setStrokeColor(colors.HexColor('#dee2e6'))
#     c.rect(right_margin - info_box_width, y - info_box_height, info_box_width, info_box_height, fill=False, stroke=True)
#     c.setFont(*ROW_FONT)
#     c.drawRightString(right_margin - 5, y - 17, f"Invoice No: #{invoice.id}")
#     c.drawRightString(right_margin - 5, y - 30, f"Date: {invoice.created_at:%d-%m-%Y}")
#     y -= 20 * mm

#     # --- Customer Info ---
#     c.setFont(*SUBHEADER_FONT)
#     c.drawString(left_margin, y - 30, "Bill To:")
#     c.setFont(*ROW_FONT)
#     c.drawString(left_margin + 45, y - 30, invoice.customer_name or "Walk-in Customer")
#     y -= 15 * mm

#     # --- Payment Mode & Bill Type Boxes ---
#     box_width = 75 * mm
#     box_height = 10 * mm

#     # Payment Mode Box
#     c.setFillColor(colors.HexColor('#f8f9fa'))
#     c.rect(left_margin, y - box_height, box_width, box_height, fill=True, stroke=True)
#     c.setFillColor(colors.HexColor('#495057'))
#     c.setFont(*ROW_FONT)
#     c.drawString(left_margin + 4, y - (box_height / 2) - 2, f"Payment Mode: {getattr(invoice, 'payment_mode', 'cash').capitalize()}")

#     # Bill Type Box
#     c.setFillColor(colors.HexColor('#f8f9fa'))
#     c.rect(left_margin + box_width + 5, y - box_height, box_width, box_height, fill=True, stroke=True)
#     c.setFillColor(colors.HexColor('#495057'))
#     c.setFont(*ROW_FONT)
#     c.drawString(left_margin + box_width + 9, y - (box_height / 2) - 2, f"Bill Type: {getattr(invoice, 'bill_type', 'GST').upper()}")

#     y -= 18 * mm

#     # --- Table Setup ---
#     columns = [
#         {"title": "Sr", "width": 12 * mm, "align": "center"},
#         {"title": "Product/Sweet", "width": 50 * mm, "align": "left"},
#         {"title": "Gross (kg)", "width": 22 * mm, "align": "right"},
#         {"title": "Tray (kg)", "width": 22 * mm, "align": "right"},
#         {"title": "Count", "width": 18 * mm, "align": "right"},
#         {"title": "Unit Price", "width": 28 * mm, "align": "right"},
#         {"title": "Amount", "width": 28 * mm, "align": "right"},
#     ]
#     table_width = sum(col['width'] for col in columns)

#     # --- Table Header (Blue Row) ---
#     header_height = 9 * mm
#     c.setFillColor(colors.HexColor('#2c3e50'))
#     c.rect(left_margin, y - header_height, table_width, header_height, fill=True, stroke=False)
#     c.setFillColor(colors.white)
#     c.setFont(*ROW_FONT)
#     x_pos = left_margin
#     for col in columns:
#         y_text = y - (header_height / 2) - 2
#         if col["align"] == "left":
#             c.drawString(x_pos + 2, y_text, col["title"])
#         elif col["align"] == "center":
#             c.drawCentredString(x_pos + col["width"] / 2, y_text, col["title"])
#         else:
#             c.drawRightString(x_pos + col["width"] - 2, y_text, col["title"])
#         x_pos += col["width"]
#     y -= header_height + 3 * mm

#     # --- Table Rows ---
#     for idx, item in enumerate(invoice.items.select_related("sweet").all(), start=1):
#         if y < 40 * mm:
#             c.showPage()
#             y = height - 30 * mm
#             c.setFont(*ROW_FONT)

#         row_height = 8 * mm
#         c.setFillColor(colors.HexColor('#f8f9fa') if idx % 2 == 0 else colors.white)
#         c.rect(left_margin, y - row_height, table_width, row_height, fill=True, stroke=True)

#         sweet = item.sweet
#         gross = Decimal(item.gross_weight_kg or 0)
#         tray = Decimal(item.tray_weight_kg or 0)
#         count = Decimal(item.count or 0)
#         net = max(gross - tray, Decimal("0.00"))
#         price = item.unit_price_override or (
#             sweet.price_per_kg if sweet.sweet_type == "weight" else sweet.price_per_unit
#         ) or Decimal("0.00")
#         amount = (net if sweet.sweet_type == "weight" else count) * price

#         values = [
#             str(idx),
#             sweet.name,
#             f"{gross:.3f}" if sweet.sweet_type == "weight" else "-",
#             f"{tray:.3f}" if sweet.sweet_type == "weight" else "-",
#             str(int(count)) if sweet.sweet_type == "count" else "-",
#             f"Rs. {price:.2f}",
#             f"Rs. {amount:.2f}"
#         ]

#         c.setFillColor(colors.HexColor('#2c3e50'))
#         c.setFont(*ROW_FONT)
#         x_pos = left_margin
#         y_text = y - (row_height / 2) - 2
#         for col, val in zip(columns, values):
#             if col["align"] == "left":
#                 c.drawString(x_pos + 2, y_text, val)
#             elif col["align"] == "center":
#                 c.drawCentredString(x_pos + col["width"]/2, y_text, val)
#             else:
#                 c.drawRightString(x_pos + col["width"] - 2, y_text, val)
#             x_pos += col["width"]
#         y -= row_height + 2

#     y -= 10 * mm

#     # --- Totals Section (Right-aligned to "Amount" column) ---
#     amount_col_right = left_margin + sum(col['width'] for col in columns[:-1]) + columns[-1]['width']
#     right_align_x = left_margin + sum(col['width'] for col in columns[:-1]) + columns[-1]['width'] - 2

#     subtotal = sum(
#         (max(Decimal(i.gross_weight_kg or 0) - Decimal(i.tray_weight_kg or 0), Decimal("0.00"))
#          * (i.unit_price_override or i.sweet.price_per_kg or Decimal("0.00"))
#          if i.sweet.sweet_type == 'weight' else
#          Decimal(i.count or 0) * (i.unit_price_override or i.sweet.price_per_unit or Decimal("0.00")))
#         for i in invoice.items.all()
#     )

#     discount_pct = Decimal(invoice.discount_percent or 0)
#     discount_amount = subtotal * discount_pct / Decimal("100.00")
#     subtotal_after_discount = subtotal - discount_amount

#     bill_type = getattr(invoice, "bill_type", "GST")
#     gst_enabled = bill_type.upper() == "GST"

#     if gst_enabled:
#         sgst = subtotal_after_discount * Decimal("2.5") / 100
#         cgst = subtotal_after_discount * Decimal("2.5") / 100
#         total = subtotal_after_discount + sgst + cgst
#     else:
#         sgst = cgst = Decimal("0.00")
#         total = subtotal_after_discount

#     c.setFillColor(colors.HexColor('#2c3e50'))
#     c.setFont(*ROW_FONT)
#     c.drawRightString(right_align_x, y, f"Subtotal: Rs. {subtotal:.2f}")
#     y -= 6 * mm
#     if discount_pct > 0:
#         c.drawRightString(right_align_x, y, f"Discount ({discount_pct}%): Rs. {discount_amount:.2f}")
#         y -= 6 * mm
#     if gst_enabled:
#         c.drawRightString(right_align_x, y, f"SGST (2.5%): Rs. {sgst:.2f}")
#         y -= 6 * mm
#         c.drawRightString(right_align_x, y, f"CGST (2.5%): Rs. {cgst:.2f}")
#         y -= 6 * mm

#     c.setFont(*TOTAL_FONT)
#     c.drawRightString(right_align_x, y, f"TOTAL: Rs. {total:.2f}")
#     y -= 15 * mm

#     # --- Footer ---
#     c.setStrokeColor(colors.HexColor('#dee2e6'))
#     c.line(left_margin, y, right_margin, y)
#     y -= 10 * mm
#     c.setFont(*ROW_FONT)
#     c.setFillColor(colors.HexColor('#6c757d'))
#     c.drawCentredString(width / 2, y, "Thank you for your business!")
#     y -= 8 * mm
#     c.setFont(*SMALL_FONT)
#     c.drawCentredString(width / 2, y, "• All prices are inclusive of applicable taxes")
#     y -= 5 * mm
#     c.drawCentredString(width / 2, y, "• Please retain this invoice for your records")
#     y -= 5 * mm
#     c.drawCentredString(width / 2, y, "• For queries, contact: 9822066728")

#     c.showPage()
#     c.save()
#     pdf = buffer.getvalue()
#     buffer.close()
#     filename = f"invoice_{invoice.id}.pdf"
#     return pdf, filename



from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from decimal import Decimal
import os

def render_invoice_pdf(invoice):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- Fonts ---
    HEADER_FONT = ("Helvetica-Bold", 18)
    COMPANY_FONT = ("Helvetica-Bold", 14)
    SUBHEADER_FONT = ("Helvetica-Bold", 12)
    ROW_FONT = ("Helvetica", 10)
    SMALL_FONT = ("Helvetica", 9)
    TOTAL_FONT = ("Helvetica-Bold", 11)

    # --- Margins ---
    left_margin = 15 * mm
    right_margin = width - 15 * mm
    y = height - 20 * mm

    # --- Company Header (Left Side) ---
    c.setFont(*COMPANY_FONT)
    c.setFillColor(colors.HexColor('#2c3e50'))
    c.drawString(left_margin, y, "TAX INVOICE")
    c.drawString(left_margin, y-30, "LALJI CATERERS")
    c.setFont(*ROW_FONT)
    c.setFillColor(colors.HexColor('#495057'))
    c.drawString(left_margin, y - 42, "GMC college Yamuna sankul, New Radhakisan Plots, Akola, Maharashtra 444001")
    c.drawString(left_margin, y - 54, "Mobile: 9422959713")
    c.drawString(left_margin, y - 66, "GSTIN: 27ABCDE1234Z5Z")

    # --- Logo (Right Side) ---
    logo_path = r"C:\Users\mohit\OneDrive\Documents\Desktop\Invoice generator\frontend\Lalji Logo.jpg"
    if os.path.exists(logo_path):
        try:
            logo_img = ImageReader(logo_path)
            iw, ih = logo_img.getSize()
            # Larger logo size
            max_w, max_h = 100 * mm, 250 * mm
            scale = min(max_w / iw, max_h / ih)
            draw_w, draw_h = iw * scale, ih * scale
            # Position on right side, aligned with company info
            logo_x = right_margin - draw_w
            c.drawImage(logo_img, logo_x+87, y - draw_h + 40, width=draw_w, height=draw_h, mask='auto')
        except Exception:
            pass

    # Divider line
    y -= 50 * mm
    c.setStrokeColor(colors.HexColor('#dee2e6'))
    c.setLineWidth(1)
    c.line(left_margin, y, right_margin, y)

    # --- TAX INVOICE Box (below line) ---
    y -= 10 * mm
    box_w, box_h = 75 * mm, 20 * mm
    box_x = right_margin - box_w
    # c.setFillColor(colors.HexColor('#f8f9fa'))
    # c.setStrokeColor(colors.HexColor('#dee2e6'))
    # c.rect(box_x, y - box_h, box_w, box_h, fill=True, stroke=True)

    # 🧾 Invoice Info (Single Line)
    c.setFont(*ROW_FONT)
    c.setFillColor(colors.HexColor('#2c3e50'))

    info_y = y - 30  # vertical position
    start_x = box_x - 297  # left margin

    invoice_text = f"Invoice No: INV-{invoice.id}"
    date_text = f"Invoice Date: {invoice.created_at:%d-%m-%Y}"
    dm_text = f"Invoice DM No: {invoice.dm_no or '-'}"

    # Draw them in one line with proper spacing
    c.drawString(start_x, info_y, invoice_text)
    c.drawString(start_x + 150, info_y, date_text)
    c.drawString(start_x + 300, info_y, dm_text)

    # --- Bill To ---
    c.setFont(*SUBHEADER_FONT)
    c.setFillColor(colors.HexColor('#2c3e50'))
    c.drawString(left_margin, y - 8, "Bill To:")
    c.setFont(*ROW_FONT)
    c.setFillColor(colors.HexColor('#495057'))
    c.drawString(left_margin + 18 * mm, y - 8, invoice.customer_name or "Walk-in Customer")

    y -= 28 * mm

    # --- Payment Info ---
    box_w = 65 * mm
    box_h = 10 * mm
    c.setStrokeColor(colors.HexColor('#dee2e6'))
    c.setFillColor(colors.HexColor('#f8f9fa'))
    # Payment box
    c.rect(left_margin, y - box_h, box_w, box_h, fill=True, stroke=True)
    c.setFont(*ROW_FONT)
    c.setFillColor(colors.HexColor('#2c3e50'))
    c.drawString(left_margin + 3, y - 18, f"Payment Mode: {getattr(invoice, 'payment_mode', 'Cash').capitalize()}")
    # Bill type box
    c.setFillColor(colors.HexColor('#f8f9fa'))
    c.rect(left_margin + box_w + 5, y - box_h, box_w, box_h, fill=True, stroke=True)
    c.setFillColor(colors.HexColor('#2c3e50'))
    c.drawString(left_margin + box_w + 8, y - 18, f"Bill Type: {getattr(invoice, 'bill_type', 'GST').upper()}")

    y -= 18 * mm

    # --- Table Header ---
    columns = [
        {"title": "Sr", "width": 12 * mm, "align": "center"},
        {"title": "Product/Sweet", "width": 55 * mm, "align": "left"},
        {"title": "Gross (kg)", "width": 22 * mm, "align": "right"},
        {"title": "Tray (kg)", "width": 22 * mm, "align": "right"},
        {"title": "Count", "width": 18 * mm, "align": "right"},
        {"title": "Unit Price", "width": 28 * mm, "align": "right"},
        {"title": "Amount", "width": 28 * mm, "align": "right"},
    ]
    table_width = sum(col['width'] for col in columns)

    header_h = 9 * mm
    c.setFillColor(colors.HexColor('#2c3e50'))
    c.rect(left_margin, y - header_h, table_width, header_h, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont(*ROW_FONT)
    x_pos = left_margin
    for col in columns:
        y_text = y - (header_h / 2) - 2
        if col["align"] == "left":
            c.drawString(x_pos + 3, y_text, col["title"])
        elif col["align"] == "center":
            c.drawCentredString(x_pos + col["width"] / 2, y_text, col["title"])
        else:
            c.drawRightString(x_pos + col["width"] - 3, y_text, col["title"])
        x_pos += col["width"]
    y -= header_h + 3 * mm

    # --- Table Rows ---
    c.setFont(*ROW_FONT)
    for idx, item in enumerate(invoice.items.select_related("sweet").all(), start=1):
        if y < 40 * mm:
            c.showPage()
            y = height - 30 * mm
            c.setFont(*ROW_FONT)

        row_h = 8 * mm
        c.setFillColor(colors.HexColor('#f8f9fa') if idx % 2 == 0 else colors.white)
        c.rect(left_margin, y - row_h, table_width, row_h, fill=True, stroke=True)

        sweet = item.sweet
        gross = Decimal(item.gross_weight_kg or 0)
        tray = Decimal(item.tray_weight_kg or 0)
        count = Decimal(item.count or 0)
        net = max(gross - tray, Decimal("0.00"))
        price = item.unit_price_override or (
            sweet.price_per_kg if sweet.sweet_type == "weight" else sweet.price_per_unit
        ) or Decimal("0.00")
        amount = (net if sweet.sweet_type == "weight" else count) * price

        values = [
            str(idx),
            sweet.name,
            f"{gross:.3f}" if sweet.sweet_type == "weight" else "-",
            f"{tray:.3f}" if sweet.sweet_type == "weight" else "-",
            str(int(count)) if sweet.sweet_type == "count" else "-",
            f"Rs. {price:.2f}",
            f"Rs. {amount:.2f}"
        ]

        c.setFillColor(colors.HexColor('#2c3e50'))
        x_pos = left_margin
        y_text = y - (row_h / 2) - 2
        for col, val in zip(columns, values):
            if col["align"] == "left":
                c.drawString(x_pos + 3, y_text, val)
            elif col["align"] == "center":
                c.drawCentredString(x_pos + col["width"] / 2, y_text, val)
            else:
                c.drawRightString(x_pos + col["width"] - 3, y_text, val)
            x_pos += col["width"]
        y -= row_h + 2

    y -= 10 * mm

    # --- Calculate totals ---
    subtotal = sum(
        (max(Decimal(i.gross_weight_kg or 0) - Decimal(i.tray_weight_kg or 0), Decimal("0.00"))
         * (i.unit_price_override or i.sweet.price_per_kg or Decimal("0.00"))
         if i.sweet.sweet_type == 'weight' else
         Decimal(i.count or 0) * (i.unit_price_override or i.sweet.price_per_unit or Decimal("0.00")))
        for i in invoice.items.all()
    )

    discount_pct = Decimal(invoice.discount_percent or 0)
    discount_amount = subtotal * discount_pct / Decimal("100.00")
    subtotal_after_discount = subtotal - discount_amount
    bill_type = getattr(invoice, "bill_type", "GST")
    gst_enabled = bill_type.upper() == "GST"

    if gst_enabled:
        sgst = subtotal_after_discount * Decimal("2.5") / 100
        cgst = subtotal_after_discount * Decimal("2.5") / 100
        total = subtotal_after_discount + sgst + cgst
    else:
        sgst = cgst = Decimal("0.00")
        total = subtotal_after_discount

    # --- Totals aligned with Amount column ---
    amount_col_start = left_margin + sum(col["width"] for col in columns[:-1])
    amount_col_width = columns[-1]["width"]
    totals_right_x = amount_col_start + amount_col_width - 3

    c.setFont(*ROW_FONT)
    c.setFillColor(colors.HexColor('#2c3e50'))
    line_gap = 6 * mm
    
    c.drawRightString(totals_right_x, y, f"Subtotal: Rs. {subtotal:.2f}")
    y -= line_gap
    if discount_pct > 0:
        c.drawRightString(totals_right_x, y, f"Discount ({discount_pct}%): Rs. {discount_amount:.2f}")
        y -= line_gap
    if gst_enabled:
        c.drawRightString(totals_right_x, y, f"SGST (2.5%): Rs. {sgst:.2f}")
        y -= line_gap
        c.drawRightString(totals_right_x, y, f"CGST (2.5%): Rs. {cgst:.2f}")
        y -= line_gap

    # --- TOTAL Section ---
    c.setFont(*TOTAL_FONT)
    c.setFillColor(colors.black)

    # Draw black line above TOTAL
    line_left = left_margin + sum(col['width'] for col in columns[:-1]) + 5  # start near amount column
    line_right = right_margin - 5
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(line_left-40, y + 12, line_right+20, y + 12)

    # Draw TOTAL text
    c.drawRightString(totals_right_x, y, f"TOTAL: Rs. {total:.2f}")

    # Draw black line below TOTAL
    c.line(line_left-40, y - 6, line_right+20, y - 6)

    y -= 15 * mm

    # --- Signature Section ---
    c.setStrokeColor(colors.HexColor('#dee2e6'))
    c.line(left_margin, y, right_margin, y)
    y -= 15 * mm
    
    # Authorized Signature on right
    sig_x = right_margin - 50 * mm
    c.setFont(*ROW_FONT)
    c.setFillColor(colors.HexColor('#2c3e50'))
    c.drawString(sig_x, y-60, "Authorized Signatory")
    c.setStrokeColor(colors.HexColor('#495057'))
    c.line(sig_x, y - 15 * mm, right_margin - 5 * mm, y - 15 * mm)
    
    y -= 30 * mm

    # --- Footer ---
    c.setStrokeColor(colors.HexColor('#dee2e6'))
    c.line(left_margin, y, right_margin, y)
    y -= 8 * mm
    c.setFont(*ROW_FONT)
    c.setFillColor(colors.HexColor('#6c757d'))
    c.drawCentredString(width / 2, y, "Thank you for your business!")
    y -= 6 * mm
    c.setFont(*SMALL_FONT)
    c.drawCentredString(width / 2, y, "• All prices are inclusive of applicable taxes")
    y -= 4 * mm
    c.drawCentredString(width / 2, y, "• Please retain this invoice for your records")
    y -= 4 * mm
    c.drawCentredString(width / 2, y, "• For queries, contact: 9822066728")
    y -= 4 * mm
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width / 2, y, "This is a computer-generated invoice and does not require a physical signature")

    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    filename = f"invoice_{invoice.id}.pdf"
    return pdf, filename