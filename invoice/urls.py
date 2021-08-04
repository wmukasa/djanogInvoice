from django.urls import path
from wkhtmltopdf.views import PDFTemplateView
from .views import (
                    login,
                    homeListView,
                    invoiceDetailView,
                    invoiceDView,
                    create_book_normal,
                    InvoiceCreate,
                    createInvoice,
                    invoiceUpdateView,
                    invoicePDFView,
                    invoicePDFView2,
                    proformaView,ProformainvoicePDFView,ProformainvoicePDFView2,
                    InvoiceDeleteView
                    )
from .import views
urlpatterns = [
    #path('', views.login,name='firm-login'),
    path('',homeListView.as_view(),name='firm-home'),
    path('<int:pk>/update',views.invoice_update,name='invoice_update22'),
    path('<int:pk>/EditDisbursement',views.disbursementUpdate,name='DisburUpdate'),
    #path('<int:pk>/update',views.update,name='update22'),
    path('dashboard/',homeListView.as_view(),name='firm-home'),
    #path('<int:pk>/details',invoiceDetailView.as_view(),name='invoice-details'),
    path('<int:pk>/details',invoiceDView.as_view(),name='invoice-details'),
    #path('createInvoice/',views.InvoiceCreate,name='create-invoice'),
    path('createInvoice3/',views.create_book_normal,name='create-invoice'),
    #path('createInvoice/',InvoiceCreate.as_view(),name='create-invoice'),
    path('createInvoice2/',views.create_invoice_with_items,name='create-invoice2'),
    #Used class based function to creating the invoice
    path('createInvoice/',createInvoice.as_view(),name='create-invoice3'),
    path('createInvoiceDis/',views.create_disbursements,name='createDisb'),
    path('<int:pk>/update', invoiceUpdateView.as_view(), name='update_invoice'),
    path('<int:pk>/invoicePdf',invoicePDFView.as_view(),name='invoice_pdf'),
    path('<int:pk>/invoicePdf2',invoicePDFView2.as_view(),name='invoice_pdf2'),
    path('<int:pk>/proformaInvoice',proformaView.as_view(),name='proforma-details'),
    path('<int:pk>/proformaInvoicePdf',ProformainvoicePDFView.as_view(),name='Proformainvoice_pdf'),
    path('<int:pk>/proformaInvoicePdf2',ProformainvoicePDFView2.as_view(),name='Proformainvoice_pdf2'),
    path('<int:pk>/DeleteInvoice',InvoiceDeleteView.as_view(), name='invoice_delete'),

    
]
