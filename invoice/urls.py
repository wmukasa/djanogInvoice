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
                    invoicePDFView2
                    )
from .import views
urlpatterns = [
    #path('', views.login,name='firm-login'),
    path('',homeListView.as_view(),name='firm-home'),
    path('dashboard/',homeListView.as_view(),name='firm-home'),
    #path('<int:pk>/details',invoiceDetailView.as_view(),name='invoice-details'),
    path('<int:pk>/details',invoiceDView.as_view(),name='invoice-details'),
    #path('createInvoice/',views.InvoiceCreate,name='create-invoice'),
    path('createInvoice/',views.create_book_normal,name='create-invoice'),
    #path('createInvoice/',InvoiceCreate.as_view(),name='create-invoice'),
    path('createInvoice2/',views.create_invoice_with_items,name='create-invoice2'),
    #Used class based function to creating the invoice
    path('createInvoice3/',createInvoice.as_view(),name='create-invoice3'),
    path('createInvoiceDis/',views.create_disbursements,name='createDisb'),
    path('<int:pk>/update', invoiceUpdateView.as_view(), name='update_invoice'),
    path('<int:pk>/invoicePdf',invoicePDFView.as_view(),name='invoice_pdf'),
    path('<int:pk>/invoicePdf2',invoicePDFView2.as_view(),name='invoice_pdf2'),
]
