# from rest_framework import viewsets, decorators
# from django.http import HttpResponse
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, JSONParser
# from .models import Sweet, Invoice
# from .serializers import SweetSerializer, InvoiceSerializer
# from .pdf import render_invoice_pdf


# class SweetViewSet(viewsets.ModelViewSet):
#     queryset = Sweet.objects.all().order_by('name')
#     serializer_class = SweetSerializer
#     parser_classes = [MultiPartParser, JSONParser]

#     @decorators.action(detail=False, methods=['get'])
#     def export_excel(self, request):
#         from .excel import export_sweets_to_excel
#         excel_bytes = export_sweets_to_excel(self.get_queryset())
#         resp = HttpResponse(excel_bytes, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         resp['Content-Disposition'] = 'attachment; filename="sweets.xlsx"'
#         return resp

#     @decorators.action(detail=False, methods=['post'])
#     def import_excel(self, request):
#         from .excel import import_sweets_from_excel
#         if 'file' not in request.FILES:
#             return Response({'detail': 'No file uploaded with field name "file"'}, status=400)
#         uploaded = request.FILES['file'].read()
#         count = import_sweets_from_excel(uploaded)
#         return Response({'imported_or_updated': count})


# class InvoiceViewSet(viewsets.ModelViewSet):
#     queryset = Invoice.objects.all().order_by('-created_at')
#     serializer_class = InvoiceSerializer

#     @decorators.action(detail=True, methods=['get'])
#     def pdf(self, request, pk=None):
#         invoice = self.get_object()
#         print(invoice.__dict__)
#         pdf_bytes, filename = render_invoice_pdf(invoice)
#         resp = HttpResponse(pdf_bytes, content_type='application/pdf')
#         resp['Content-Disposition'] = f'attachment; filename="{filename}"'
#         return resp

#     @decorators.action(detail=True, methods=['get'])
#     def export_excel(self, request, pk=None):
#         from .excel import export_invoice_to_excel
#         invoice = self.get_object()
#         excel_bytes = export_invoice_to_excel(invoice)
#         resp = HttpResponse(excel_bytes, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         resp['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.xlsx"'
#         return resp


from rest_framework import viewsets, decorators
from rest_framework.parsers import MultiPartParser, JSONParser
from django.http import HttpResponse
from rest_framework.response import Response
from .models import Sweet, Invoice
from .serializers import SweetSerializer, InvoiceSerializer
from .pdf import render_invoice_pdf


class SweetViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Sweets. Exports/imports Excel.
    """
    queryset = Sweet.objects.all().order_by('name')
    serializer_class = SweetSerializer
    parser_classes = [MultiPartParser, JSONParser]  # support JSON and multipart

    @decorators.action(detail=False, methods=['get'])
    def export_excel(self, request):
        from .excel import export_sweets_to_excel
        excel_bytes = export_sweets_to_excel(self.get_queryset())
        resp = HttpResponse(
            excel_bytes,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        resp['Content-Disposition'] = 'attachment; filename="sweets.xlsx"'
        return resp

    @decorators.action(detail=False, methods=['post'])
    def import_excel(self, request):
        from .excel import import_sweets_from_excel
        if 'file' not in request.FILES:
            return Response({'detail': 'No file uploaded with field name "file"'}, status=400)
        uploaded = request.FILES['file'].read()
        count = import_sweets_from_excel(uploaded)
        return Response({'imported_or_updated': count})


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Invoices with PDF and Excel export.
    Handles invoice items by sweet name (duplicate allowed).
    """
    queryset = Invoice.objects.all().order_by('-created_at')
    serializer_class = InvoiceSerializer
    parser_classes = [JSONParser, MultiPartParser]

    @decorators.action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        invoice = self.get_object()
        pdf_bytes, filename = render_invoice_pdf(invoice)
        resp = HttpResponse(pdf_bytes, content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="{filename}"'
        return resp

    @decorators.action(detail=True, methods=['get'])
    def export_excel(self, request, pk=None):
        from .excel import export_invoice_to_excel
        invoice = self.get_object()
        excel_bytes = export_invoice_to_excel(invoice)
        resp = HttpResponse(
            excel_bytes,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        resp['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.xlsx"'
        return resp
