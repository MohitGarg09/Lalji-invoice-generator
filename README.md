# Invoice Generator (Django + DRF)

An API-driven invoice generator for a sweets shop.

- By weight: amount = max((gross_g - tray_g), 0) / 1000 × price_per_kg
- By count: amount = count × price_per_unit

## Features
- Manage sweets catalog (weight or count)
- Create invoices with mixed items
- Subtotal, discount, final total
- PDF generation for invoices
- Excel import/export (sweets) and invoice export
- Admin for data entry

## Tech
- Django, Django REST Framework, django-cors-headers
- SQLite (dev), ReportLab (PDF), openpyxl (Excel)

## Layout
- `backend/` Django project
  - `backend/` settings/urls
  - `billing/` models, serializers, views, urls, pdf, excel, admin
- `frontend/` optional Vite scaffold (not required)

## Quick Start (Windows PowerShell)
```powershell
cd "C:\Users\mohit\OneDrive\Documents\Desktop\Invoice generator"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install django djangorestframework django-cors-headers reportlab openpyxl pandas
python backend\manage.py makemigrations
python backend\manage.py migrate
python backend\manage.py runserver 127.0.0.1:8000
```
Open `http://127.0.0.1:8000/api/`.

### Admin (optional)
```powershell
python backend\manage.py createsuperuser
```
Visit `http://127.0.0.1:8000/admin/` (models: Sweet, Invoice, InvoiceItem).

## API
Base: `http://127.0.0.1:8000/api/`

### Sweets
- GET `/sweets/`
- POST `/sweets/`
- GET `/sweets/{id}/`
- PUT/PATCH `/sweets/{id}/`
- DELETE `/sweets/{id}/`
- GET `/sweets/export_excel/`
- POST `/sweets/import_excel/` (multipart field `file`)

### Invoices
- GET `/invoices/`
- POST `/invoices/`
- GET `/invoices/{id}/`
- PUT/PATCH `/invoices/{id}/`
- DELETE `/invoices/{id}/`
- GET `/invoices/{id}/pdf/`
- GET `/invoices/{id}/export_excel/`

## Models
- Sweet: `name`, `sweet_type` (`weight|count`), `price_per_kg?`, `price_per_unit?`
- Invoice: `customer_name?`, `discount_amount`, computed `subtotal`, `total`
- InvoiceItem: `sweet`, weight fields (`gross_weight_g`, `tray_weight_g`) or `count`; computed `net_weight_g`, `total_amount`

## Calculation
- Weight: `net_g = max(gross - tray, 0)`; `amount = (net_g/1000) * price_per_kg`
- Count: `amount = count * price_per_unit`
- Invoice: `total = max(subtotal - discount, 0)`

## cURL Examples
Create weight sweet:
```bash
curl -H "Content-Type: application/json" -d '{"name":"Kaju Katli","sweet_type":"weight","price_per_kg":"800.00"}' http://127.0.0.1:8000/api/sweets/
```
Create count sweet:
```bash
curl -H "Content-Type: application/json" -d '{"name":"Rasgulla","sweet_type":"count","price_per_unit":"20.00"}' http://127.0.0.1:8000/api/sweets/
```
Create invoice:
```bash
curl -H "Content-Type: application/json" -d '{"customer_name":"Akash","discount_amount":"20.00","items":[{"sweet":1,"gross_weight_g":"850","tray_weight_g":"50"},{"sweet":2,"count":12}]}' http://127.0.0.1:8000/api/invoices/
```
PDF:
```bash
curl -L -o invoice_1.pdf http://127.0.0.1:8000/api/invoices/1/pdf/
```
Invoice Excel:
```bash
curl -L -o invoice_1.xlsx http://127.0.0.1:8000/api/invoices/1/export_excel/
```
Sweets Excel export:
```bash
curl -L -o sweets.xlsx http://127.0.0.1:8000/api/sweets/export_excel/
```
Sweets Excel import (headers: name, sweet_type, price_per_kg, price_per_unit):
```bash
curl -X POST -F "file=@sweets.xlsx" http://127.0.0.1:8000/api/sweets/import_excel/
```

## Troubleshooting
- Use explicit venv python on Windows:
```powershell
& ".\.venv\Scripts\python.exe" "backend\manage.py" runserver 127.0.0.1:8000
```
- CORS open for dev (see `backend/backend/settings.py`).
- Ensure superuser exists for admin.

## Production
- Switch to Postgres/MySQL, add auth/permissions, tighten CORS/CSRF, serve via nginx + gunicorn/uvicorn.

## License
Private/internal use.
