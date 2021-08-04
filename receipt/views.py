from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime,date
from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse
from .forms import receiptCreateForm,receiptCreateModelForm
from .models import receipts
from django_pdfkit import PDFView
from .utils import render_to_pdf
from django.template.loader import get_template
from wkhtmltopdf.views import PDFTemplateResponse 

from django.views.generic import (ListView,DetailView,CreateView,View,
                                    DeleteView,UpdateView)
import os, sys, subprocess, platform
import pdfkit
   
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
'''
def ourReceipts(request):
    context = {
        'myreceipt':receipts.objects.all()
    }
    return render(request,'receipt/ourReceiptPage.html',context)
'''
class ourReceiptsListView(ListView):
    model = receipts
    paginate_by = 3
    ordering=['-date_created'] 
    template_name = 'receipt/ourReceiptPage.html'
 	  
class receiptDetailView(DetailView):
    model = receipts
    template_name = 'receipt/receipt.html'

    def get_absolute_url(self):
        return reverse('receipt-details', kwargs={'pk':self.pk})

class createReceiptView(View):
    def get(self,*args,**kwargs):
        #form
        form =receiptCreateForm()
        context={
            'form':form
        }
        return render(self.request,"receipt/receipt_form.html",context)
    '''
    def post(self,*args,**kwargs):

        #print(self.request.POST)
        if self.request.method == 'POST':
            form =receiptCreateForm(self.request.POST or None)
            print("The form is valid")
            #print(form.cleaned_data)
            receipt_number = self.request.POST['receipt_number']
            received_from = self.request.POST['received_from']
            sum_in_words = self.request.POST['sum_in_words']
            reason = self.request.POST['reason']
            cash_cheque = self.request.POST['cash_cheque']
            balance = self.request.POST['balance']
            amount = self.request.POST['amount']
            #print("Hello William")
            print(amount)
            #return redirect('our_receipts')
        #messages.warning(self.request,"Failed to create your receipt")
        return redirect('our_receipts')
    '''
    def post(self,*args,**kwargs):
        form = receiptCreateForm(self.request.POST or None)
        try:
            get_id = receipts.objects.order_by('-id').first()
            x: int = get_id.id + 1
            y = date.today().strftime("%y%m")
            if get_id:
                receipt_number = "" + y + str(x).zfill(3) + ""  
        except:
            receipt_number = str(date.today().strftime("%y%m") + str(1).zfill(3))  
        finally: 
            if form.is_valid():
                receipt_number = receipt_number
                date_created = form.cleaned_data.get('date_created')
                received_from = form.cleaned_data.get('received_from')
                sum_in_words = form.cleaned_data.get('sum_in_words')
                reason = form.cleaned_data.get('reason')
                cash_cheque = form.cleaned_data.get('cash_cheque')
                balance = form.cleaned_data.get('balance')
                amount = form.cleaned_data.get('amount')
                #print(date_created)
                receipt_data = receipts(receipt_number=receipt_number,received_from=received_from,date_created=date_created,
                                        sum_in_words=sum_in_words,reason=reason,cash_cheque=cash_cheque,
                                        balance=balance,amount=amount,author=self.request.user)
                receipt_data.save()
                messages.info(self.request,"This receipt was saved.")
                return redirect('our_receipts')
            messages.info(self.request,"This receipt was not saved.")
            return redirect('our_receipts')
# another way of creating using raw create class based view
class createReceipt2View(View):
    template_name = "receipt/receipt_form.html"
    #GET METHOD
    def get(self,request,*args,**kwargs):
        form = receiptCreateModelForm()
        context={
            'form':form
        }
        return render(request,self.template_name,context)
    #POST METHOD
    def post(self,request,*args,**kwargs):
        form = receiptCreateModelForm(request.POST)
        context={
            'form':form
        }
        if form.is_valid():
            form.save()
        return render(request,self.template_name,context)

#class based view works for update but without customed form fields          
class receiptUpdateView(LoginRequiredMixin,UpdateView):
	model = receipts 
	fields =['received_from','date_created','sum_in_words','reason','cash_cheque','balance','amount']
	template_name = 'receipt/receipt_form.html'

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)
#class based view works for update with customed form fields, working for this app
class receiptUpdateModelView(UpdateView):
    template_name='receipt/receipt_form.html'
    form_class = receiptCreateModelForm
    queryset = receipts.objects.all()
    def form_valid(self,form):
        return super().form_valid(form)

        
#deleting using class based view
class receiptDeleteView(DeleteView):
    template_name = 'receipt/receipt_formDelete.html'
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(receipts,pk=pk)
    
    def get_success_url(self):
        messages.info(self.request,"You have deleted a receipt.")
        return reverse('our_receipts')


#deleting using a function, the working function for the app
def receipt_delete_view(request,id):
    obj = get_object_or_404(receipt,pk=pk)
    if request.method =='POST':
        obj.delete()
        return redirect('our_receipts')
    return render(request,'receipt/ourReceiptPage.html')


#Illustration of function based view to class based view
class receiptUpdateView2(View):
    template_name = 'receipt/receipt_form.html'
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj =None
        if pk is not None:
            obj = get_object_or_404(receipts,pk=pk)
        return obj
    def get(self,request,pk =None,*args,**kwargs):
        context ={}
        obj =self.get_object()  
        if obj is not None:
            form =receiptCreateForm(instance=obj)
            context['object'] =obj
            context['form'] =form
        return render(request,self.template_name,context)
    
    def post(self,request,pk=None,*args,**kwargs):
        context ={}
        obj = self.get_object()
        if obj is not None:
            form=receiptCreateForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
            context['object'] =obj
            context['form'] =form
        return render(request,self.template_name,context)
'''
class receiptPdf(LoginRequiredMixin,PDFView):
    template_name = 'receipt/receipt_pdf.html'
    def get_receipt_pdf(self,*args,**kwargs):
        context = super().get_receipt_pdf(*args,**kwargs)
        context['receipts']=receipts.objects.filter(id = kwargs['pk'],
        )
        return context 
'''
#this class based function creates a pdf with render_to_pdf
class receiptPdf(View):
    def get(self,request,*args,**kwargs):
        template = get_template('receipt/receipt_pdf.html')
        context={
            "date_created": '2021-05-06',
            "receipt_number":'2105001',
            "received_from":'Mukasa Willy',
            "sum_in_words":'Hundred Million Shillings Only',
            "reason":'House building',
            "cash_cheque":'Cash',
            "balance":'NIL',
            "amount":100000000,
        }
        html = template.render(context)
        pdf = render_to_pdf('receipt/receipt_pdf.html',context)
        return HttpResponse(pdf, content_type='application/pdf')
# class based function that creates a pdf with wkhtmltopdf module

class usingwktohtml(View):
    def get(self,request,*args,**kwargs):
        html_path = 'receipt/receipt_pdf.html'
        context={
                "date_created": '2021-05-06',
                "receipt_number":'2105001',
                "received_from":'Mukasa Willy',
                "sum_in_words":'Hundred Million Shillings Only',
                "reason":'House building',
                "cash_cheque":'Cash',
                "balance":'NIL',
                "amount":100000000,
        }
        '''
        response = PDFTemplateResponse(request=request,
                                    template=html_path,
                                    filename="hello.pdf",
                                    context= context,
                                    show_content_in_browser=False,
                                    cmd_options=settings.WKHTMLTOPDF_CMD_OPTIONS,
                                    )
        '''
        return PDFTemplateResponse(request=request, cmd_options={'disable-javascript':True}, 
                                    template=html_path, context=context)
#using pdf kit with wktohtml 
def pdf(request):
    persons = receipts.objects.all()
    template = get_template('receipt/receipt_pdf.html')
    html = template.render({'persons': persons})
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False,configuration=_get_pdfkit_config())
    response = HttpResponse(pdf, content_type='application/pdf')

    return response  
