from django.contrib import admin
from .models import Invoice,InvoiceLineItem,Disbursements

admin.site.register(Invoice)
admin.site.register(InvoiceLineItem)
admin.site.register(Disbursements)
