from django.urls import path
from .views import (ourReceiptsListView,
                    receiptDetailView,
                    receiptUpdateView2,
                    receiptUpdateModelView,
                    receiptDeleteView,
                    createReceiptView,
                    createReceipt2View,
                    receiptPdf,
                    usingwktohtml,receiptPDFView
                    )
from .import views
from django_pdfkit import PDFView
def _get_pdfkit_config():

    if platform.system() == 'Windows':
         return pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
    else:
         WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')], stdout=subprocess.PIPE).communicate()[0].strip()
         return pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
wk_options = {
        #'page-size': 'Letter',
        #'orientation': 'landscape',
        # In order to specify command-line options that are simple toggles
        # using this dict format, we give the option the value None
        'no-outline': None,
        'disable-javascript': None,
        'encoding': 'UTF-8',
        'margin-left': '0.1cm',
        'margin-right': '0.1cm',
        'margin-top': '0.1cm',
        'margin-bottom': '0.1cm',
        'lowquality': None,
}

urlpatterns = [
    path('',ourReceiptsListView.as_view(),name='our_receipts' ), 
    path('<int:pk>/details',receiptDetailView.as_view(),name='receipt-details'),
    path('newReceipt/',createReceiptView.as_view(),name='receipt-create'),
    #path('receipt/<int:pk>/update', receiptUpdateView2.as_view(), name='update_receipt2'),
    path('<int:pk>/update', receiptUpdateModelView.as_view(), name='update_receipt'),
    path('<int:pk>/delete', receiptDeleteView.as_view(), name='delete_receipt'),
    #used this because i used a html model to  as confirmation message for deleting 
    path('<int:pk>/delete',views.receipt_delete_view, name='delete_receipt2'),
    #alternative of creating views
    path('create/',createReceipt2View.as_view(),name='create_receipts' ), 
    #path('<int:pk>/pdf', receiptPdf.as_view(), name='receipt-pdf'),
    path('<int:pk>/pdf', PDFView.as_view(template_name='receipt/receipt_pdf.html'), name='my-pdf'),
    #using receiptPdf for pdf kit to get pdf
    path('receiptPdf1/',receiptPdf.as_view(),name='receipt-pdf1'),
    path('wktopdf/',usingwktohtml.as_view(),name='wktopdf-pdf'),
    path('kit/', views.pdf,name='kit-pdf'),
    path('<int:pk>/receiptPdf/',receiptPDFView.as_view(),name='receipt-pdf')
]