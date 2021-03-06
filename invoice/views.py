from django.contrib import messages
from django.urls import reverse,reverse_lazy
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template,render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect,get_object_or_404
from datetime import datetime,date
from django.db.models import Q 
#from .forms import invoiceCreateForm
from django.views.generic import (ListView,DetailView,CreateView,
                                    DeleteView,UpdateView,View)
from .forms import (
    InvoiceFormset,
    InvoiceLineItemModelFormset,
    InvoiceSecondModelForm,
    DisbursementsModelFormset,
    InvoiceLineItemModelForm,
    LineIteminlineFormset,
    DisbursementsinlineFormset
    )
from django.forms import (inlineformset_factory)
from .models import (Invoice,InvoiceLineItem,Disbursements)
import os, sys, subprocess, platform
import pdfkit
from wkhtmltopdf.views import PDFTemplateView
from django.forms import (formset_factory, modelformset_factory,inlineformset_factory)
from django.template import RequestContext
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
def handler404(request, *args, **argv):
    response = render('errors/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request, *args, **argv):
    response = render('errors/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
'''
def page_not_found_view(request, exception):
    return render(request, 'errors/404.html', status=404)

    
@login_required 
def login(request):
	return render(request,'users/logout.html')
class homeListView(LoginRequiredMixin,ListView):
    model = Invoice
    paginate_by = 5
    ordering=['-issue_date'] 
    template_name = 'invoice/dashboard.html'

class invoiceDetailView(LoginRequiredMixin,DetailView):
    model = Invoice
    #model = InvoiceLineItem
    template_name = 'invoice/invoice_detail.html'
    def get_absolute_url(self):
        return reverse('invoice-details', kwargs={'pk':self.pk})
    
class invoiceDView(LoginRequiredMixin,View):
    def get(self,request,pk, *args, **kwargs):
        inv_id = get_object_or_404(Invoice,pk=pk)
        VAT =0
        subtotal_pr=0
        subtotal_db = 0
        grandtotal =0
        try:
            invoice = Invoice.objects.get(ref_nwumber=inv_id)
            VAT = (18/100)*(invoice.professional_amount)
            subtotal_pr = float(VAT+invoice.professional_amount)
            dis = Disbursements.objects.filter(invoice=invoice).all()
            for q in dis:
                subtotal_db +=float(q.disbursement_amount)
            grandtotal = subtotal_pr+subtotal_db
            #print(grandtotal) 
            context = {
                'object': invoice,
                'VAT':VAT,
                'subtotal_pr':subtotal_pr,
                'subtotal_db':subtotal_db,
                'grandtotal':grandtotal 
            }
            return render(self.request,'invoice/invoice_detail.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have such an invoice")
            return redirect("/")
@login_required 
def mySearch(request):
    template_name = 'invoice/dashboard.html'
    if request.method == "POST":
        query_name = request.POST.get('tag', None)
        if query_name:
            results = Invoice.objects.filter(Q(name_to__icontains=query_name)|Q( 
                                                ref_nwumber__icontains=query_name)|Q(
                                                issue_date__icontains=query_name)|Q(
                                                company_name__icontains=query_name))
            return render(request, template_name, {"results":results})

        return render(request, template_name)
   
class SearchView(LoginRequiredMixin,ListView):  # tasklar?? arama sonucu listeliyoruz
    model = Invoice
    template_name = 'invoice/dashboard.html'
    paginate_by = 5
    #context_object_name = 'task'
    def get_queryset(self):
        query_name = self.request.GET.get("tag", None)
        if query_name:
            results = Invoice.objects.filter(Q(name_to__icontains=query_name)|Q( 
                                                ref_nwumber__icontains=query_name)|Q(
                                                issue_date__icontains=query_name)|Q(
                                                company_name__icontains=query_name))
            return render(request, template_name, {"results":results})
        return render(request, template_name)  

@login_required 
def mySearch2(request):
    template_name = 'invoice/dashboard.html'

    if request.method == "POST":
        search_invoice = request.POST.get('tag', None)
    #search_invoice=request.GET.get('tag')
        if search_invoice:
            results =Invoice.objects.filter(Q(name_to__icontains=search_invoice) | Q(ref_nwumber__icontains=search_invoice))   
        else:
            results = Invoice.objects.all().order_by("-issue_date")  
        return render(request, template_name,{'results':results})

@login_required
def InvoiceCreate(request):
    return render(request,'invoice/createInvoice.html')

class InvoiceCreate(LoginRequiredMixin,View):
    
    def get(self,*args,**kwargs):
        form = invoiceCreateForm()
        context ={
            'form':form
        }
 
        return render(self.request,'invoice/createInvoice.html',context)
@login_required
def create_book_normal(request):
    template_name = 'invoice/createInvoice.html'
    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = InvoiceFormset(request.GET or None)
    elif request.method == 'POST':
        formset = InvoiceFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # extract name from each form and save
                name = form.cleaned_data.get('name')
                # save book instance
                #if name:
                    #Book(name=name).save()
            # once all books are saved, redirect to book list view
            return redirect('firm-home')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })
@login_required
def create_invoice_with_items(request):
    template_name = 'invoice/createInvoice.html'
    if request.method == 'GET':
        bookform = InvoiceSecondModelForm(request.GET or None)
        formset =InvoiceLineItemModelFormset (queryset=InvoiceLineItem.objects.none())
    elif request.method == 'POST':
        bookform = InvoiceSecondModelForm(request.POST)
        formset = InvoiceLineItemModelFormset(request.POST)
        '''
        try:
            get_id = Invoice.objects.order_by('-id').first()
            x: int = get_id.id + 1
            y = date.today().strftime("%y%m")
            if get_id:
                ref_nwumber = "" + y + str(x).zfill(3) + ""  
        except:
            ref_nwumber = str(date.today().strftime("%y%m") + str(1).zfill(3)) 
        finally: 
        '''
        if bookform.is_valid() and formset.is_valid():
                # first save this book, as its reference will be used in `Author`
                #ref_nwumber=ref_nwumber
            invoice = bookform.save()
            for form in formset:
                # so that `invoice` instance can be attached.
                invoiceItem = form.save(commit=False)
                invoiceItem.invoice = invoice
                invoiceItem.save()
            return redirect('firm-home')
    return render(request, template_name, {
        'bookform': bookform,
        'formset': formset,

    })



class createInvoice(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        bookform = InvoiceSecondModelForm()
        formset =InvoiceLineItemModelFormset(queryset=InvoiceLineItem.objects.none())
        context={
            'bookform':bookform,
            'formset':formset
        }
        return render(self.request,"invoice/createInvoice.html",context)

    def post(self,*args,**kwargs):
        bookform = InvoiceSecondModelForm(self.request.POST or None)
        formset = InvoiceLineItemModelFormset(self.request.POST)
        try:
            get_id = Invoice.objects.order_by('-id').first()
            x: int = get_id.id + 1
            y = date.today().strftime("%y%m")
            if get_id:
                ref_nwumber = "" + y + str(x).zfill(3) + ""  
        except:
            ref_nwumber = str(date.today().strftime("%y%m") + str(1).zfill(3))  
        finally: 
            if bookform.is_valid() and formset.is_valid():
                ref_nwumber = ref_nwumber
                name_to = bookform.cleaned_data.get('name_to')
                company_name = bookform.cleaned_data.get('company_name')
                address_to = bookform.cleaned_data.get('address_to')
                telephone_to = bookform.cleaned_data.get('telephone_to')
                email_to = bookform.cleaned_data.get('email_to')
                box_number_to = bookform.cleaned_data.get('box_number_to')
                terms = bookform.cleaned_data.get('terms')
                issue_date = bookform.cleaned_data.get('issue_date')
                vat = bookform.cleaned_data.get('vat')
                bank = bookform.cleaned_data.get('bank')
                bank_branch = bookform.cleaned_data.get('bank_branch')
                swift_code = bookform.cleaned_data.get('swift_code')
                account_number = bookform.cleaned_data.get('account_number')
                professional_amount = bookform.cleaned_data.get('professional_amount')
                invoice_data = Invoice(ref_nwumber=ref_nwumber,name_to=name_to,company_name=company_name,
                                        address_to=address_to,telephone_to=telephone_to,email_to=email_to,
                                        box_number_to=box_number_to,terms=terms,issue_date=issue_date,
                                        vat=vat,bank=bank,bank_branch=bank_branch,swift_code=swift_code,
                                        account_number=account_number,professional_amount=professional_amount,
                                        author=self.request.user)
                invoice=invoice_data.save()
                for form in formset:
                    invoice = Invoice.objects.last()
                    # so that `invoice` instance can be attached.
                    lineItem = form.save(commit=False)
                    lineItem.invoice = invoice
                    lineItem.save()
                messages.info(self.request,"This invoice was saved.")
                return redirect('createDisb')
            messages.info(self.request,"This invoice was not saved.")
            return redirect('firm-home')

@login_required
def create_disbursements(request):
    template_name = 'invoice/createInvoiceDis.html'
    if request.method == 'GET':
        #formset = InvoiceFormset(request.GET or None)
        formsetDis = DisbursementsModelFormset(queryset=Disbursements.objects.none())
    elif request.method == 'POST':
        formsetDis = DisbursementsModelFormset(request.POST)
        #invoice = get_object_or_404(Invoice)
        last_id = Invoice.objects.last().id
        #print(last_id)
        if formsetDis.is_valid():
            for form in formsetDis:
                # extract name from each form and save
                disbursement_amount = form.cleaned_data.get('disbursement_amount')
                disb_heading = form.cleaned_data.get('disb_heading')
                disb_sub1 = form.cleaned_data.get('disb_sub1')
                disb_sub2 = form.cleaned_data.get('disb_sub2')
                disb_sub3 = form.cleaned_data.get('disb_sub3')
                # save book instance
                #if amount,heading,sub1,sub2,sub3:
                #invoice = get_object_or_404(Invoice,last_id)
                invoice = Invoice.objects.last()
                dis =Disbursements(disbursement_amount=disbursement_amount,disb_heading=disb_heading,
                                disb_sub1=disb_sub1,disb_sub2=disb_sub2,disb_sub3=disb_sub3,invoice=invoice)
                
                #dis.invoice = Invoice.objects.get(pk)
                #dis.invoice = invoice
                #print(invoice)
                #instance = dis.save(commit=False)
                #instance.invoice = invoice
                dis.save()
                #instance.save()
            # once all books are saved, redirect to book list view
            return redirect('firm-home')
    return render(request, template_name, {
        'formsetDis':formsetDis,
    })

class invoiceUpdateView(LoginRequiredMixin,View):
    template_name='invoice/invoiceUpdate.html'
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj =None
        if pk is not None:
            obj = get_object_or_404(Invoice,pk=pk)
        return obj
    def get(self,request,pk =None,*args,**kwargs):
        context ={}
        obj =self.get_object()  
        if obj is not None:
            bookform =InvoiceSecondModelForm(instance=obj)
            formset =InvoiceLineItemModelFormset(queryset=InvoiceLineItem.objects.filter(invoice=obj).all())
            context['object'] =obj
            context['bookform'] =bookform
            context['formset'] =formset
        return render(request,self.template_name,context)
    
    def post(self,request,pk=None,*args,**kwargs):
        context ={}
        obj = self.get_object()
        formset_config = {

            'form': InvoiceLineItemModelForm,
        }
        item = InvoiceLineItem.objects.filter(invoice=obj)
        print(item)
        #form = inlineformset_factory(Invoice,InvoiceLineItem,**formset_config)
        #invoice = Invoice()
        #print(form)

        #formset = form(queryset=item)
        #formset = form(item)
        #print(formset)
        if obj is not None and item is not None:
            bookform=InvoiceSecondModelForm(request.POST,prefix='obj')
            #formset =form(request.POST or None,request.FILES or None,queryset=item)
            #formset = form(request.POST,request.FILES, prefix='formset')
            #print(formset)
            formset = InvoiceLineItemModelFormset(self.request.POST,queryset=item)
            print(formset)
            if bookform.is_valid() and formset.is_valid():
                print('WILLIAM')
  
                #invoice=bookform.save()
                #for form in formset:
                    #invoice = Invoice.objects.last()
                    #lineItem = form.save(commit=False)
                    #lineItem.invoice = invoice
                    #print(lineItem)
                    #lineItem.save() 
            context['object'] =obj
            context['bookform'] =bookform
            context['formset'] =formset
            #return reverse('invoice-details', kwargs={'pk':self.pk})
           
        return render(request,self.template_name,context)
@login_required
def invoice_update(request, pk=None):
        if request.method == 'GET':
                instance = get_object_or_404(Invoice,pk=pk) 
                #print(instance.id)
                bookform = InvoiceSecondModelForm(request.POST or None, request.FILES or None, instance=instance)
                #formset = InvoiceLineItemModelFormset(queryset=InvoiceLineItem.objects.filter(invoice=instance).all())
                formset=LineIteminlineFormset(instance=instance)
                #formset = InvoiceLineItemModelFormset(request.POST,queryset=InvoiceLineItem.objects.filter(invoice=instance).all())
        elif request.method == 'POST':
                instance = get_object_or_404(Invoice,pk=pk)
                bookform = InvoiceSecondModelForm(request.POST,request.FILES or None, instance=instance)
                #formset = InvoiceLineItemModelFormset(request.POST,queryset=InvoiceLineItem.objects.filter(invoice=instance))
                formset = LineIteminlineFormset(request.POST,instance=instance)
                formset.save()
                if bookform.is_valid():
                    bookform.save()
                    return  redirect('DisburUpdate',pk=pk)
        
        context = {
            "instance": instance,
            "bookform": bookform,
            "formset": formset
        }
        return render(request,'invoice/invoiceUpdate.html',context)

@login_required        
def disbursementUpdate(request,pk=None):
        dis = Invoice.objects.get(pk=pk)
        formset = DisbursementsinlineFormset(instance=dis)
        if request.method == 'POST':
            formset = DisbursementsinlineFormset(request.POST,instance=dis)
            formset.save()
            return redirect('invoice-details',pk=pk)
        return render(request,'invoice/disbUpdate.html',{'formset':formset})

class invoicePDFView(LoginRequiredMixin,View):
    def get(self,request,pk, *args, **kwargs):
        inv_id = get_object_or_404(Invoice,pk=pk)
        VAT =0
        subtotal_pr=0
        subtotal_db = 0
        grandtotal =0
        try:
            invoice = Invoice.objects.get(ref_nwumber=inv_id)
            VAT = (18/100)*(invoice.professional_amount)
            subtotal_pr = float(VAT+invoice.professional_amount)
            dis = Disbursements.objects.filter(invoice=invoice).all()
            for q in dis:
                subtotal_db +=float(q.disbursement_amount)
            grandtotal = subtotal_pr+subtotal_db
            #print(grandtotal) 
            context = {
                'object': invoice,
                'VAT':VAT,
                'subtotal_pr':subtotal_pr,
                'subtotal_db':subtotal_db,
                'grandtotal':grandtotal 
            }
            template = get_template('invoice/my_invoicePdf.html')
            html = template.render(context)
            #css = ['firm/invoice/static/css/testing.css']
            pdf = pdfkit.from_string(html,False,configuration=_get_pdfkit_config(),options=wk_options)
            response = HttpResponse(pdf)
            response.headers['Content-Type']='application/pdf'
            #response.headers['Content-Disposition']='inline; filename=TaxInvoice'+str(pk)+'.pdf'
            #response = HttpResponse(pdf, content_type='application/pdf')
            return response
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have such an invoice")
            return redirect("/")
class invoicePDFView2(LoginRequiredMixin,View):
    def get(self,request,pk, *args, **kwargs):
        inv_id = get_object_or_404(Invoice,pk=pk)
        VAT =0
        subtotal_pr=0
        subtotal_db = 0
        grandtotal =0
        try:
            invoice = Invoice.objects.get(ref_nwumber=inv_id)
            VAT = (18/100)*(invoice.professional_amount)
            subtotal_pr = float(VAT+invoice.professional_amount)
            dis = Disbursements.objects.filter(invoice=invoice).all()
            for q in dis:
                subtotal_db +=float(q.disbursement_amount)
            grandtotal = subtotal_pr+subtotal_db
            #print(grandtotal) 
            context = {
                'object': invoice,
                'VAT':VAT,
                'subtotal_pr':subtotal_pr,
                'subtotal_db':subtotal_db,
                'grandtotal':grandtotal 
            }
            template = get_template('invoice/my_invoicePdf2.html')
            html = template.render(context)
            #css = ['firm/invoice/static/css/testing.css']
            pdf = pdfkit.from_string(html,False,configuration=_get_pdfkit_config(),options=wk_options)
            response = HttpResponse(pdf)
            response.headers['Content-Type']='application/pdf'
            #response.headers['Content-Disposition']='inline; filename=TaxInvoice'+str(pk)+'.pdf'
            #response = HttpResponse(pdf, content_type='application/pdf')
            return response
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have such an invoice")
            return redirect("/")
class proformaView(LoginRequiredMixin,View):
    def get(self,request,pk, *args, **kwargs):
        inv_id = get_object_or_404(Invoice,pk=pk)
        VAT =0
        subtotal_pr=0
        subtotal_db = 0
        grandtotal =0
        try:
            invoice = Invoice.objects.get(ref_nwumber=inv_id)
            VAT = (18/100)*(invoice.professional_amount)
            subtotal_pr = float(VAT+invoice.professional_amount)
            dis = Disbursements.objects.filter(invoice=invoice).all()
            for q in dis:
                subtotal_db +=float(q.disbursement_amount)
            grandtotal = subtotal_pr+subtotal_db
            #print(grandtotal) 
            context = {
                'object': invoice,
                'VAT':VAT,
                'subtotal_pr':subtotal_pr,
                'subtotal_db':subtotal_db,
                'grandtotal':grandtotal 
            }
            return render(self.request,'invoice/proformInvoice.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have such an invoice")
            return redirect("/")
class ProformainvoicePDFView(LoginRequiredMixin,View):
    def get(self,request,pk, *args, **kwargs):
        inv_id = get_object_or_404(Invoice,pk=pk)
        VAT =0
        subtotal_pr=0
        subtotal_db = 0
        grandtotal =0
        try:
            invoice = Invoice.objects.get(ref_nwumber=inv_id)
            VAT = (18/100)*(invoice.professional_amount)
            subtotal_pr = float(VAT+invoice.professional_amount)
            dis = Disbursements.objects.filter(invoice=invoice).all()
            for q in dis:
                subtotal_db +=float(q.disbursement_amount)
            grandtotal = subtotal_pr+subtotal_db
            #print(grandtotal) 
            context = {
                'object': invoice,
                'VAT':VAT,
                'subtotal_pr':subtotal_pr,
                'subtotal_db':subtotal_db,
                'grandtotal':grandtotal 
            }
            template = get_template('invoice/proformaInvoicePdf.html')
            html = template.render(context)
            #css = ['firm/invoice/static/css/testing.css']
            pdf = pdfkit.from_string(html,False,configuration=_get_pdfkit_config(),options=wk_options)
            response = HttpResponse(pdf)
            response.headers['Content-Type']='application/pdf'
            #response.headers['Content-Disposition']='inline; filename=TaxInvoice'+str(pk)+'.pdf'
            #response = HttpResponse(pdf, content_type='application/pdf')
            return response
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have such an invoice")
            return redirect("/")  
class ProformainvoicePDFView2(LoginRequiredMixin,View):
    def get(self,request,pk, *args, **kwargs):
        inv_id = get_object_or_404(Invoice,pk=pk)
        VAT =0
        subtotal_pr=0
        subtotal_db = 0
        grandtotal =0
        try:
            invoice = Invoice.objects.get(ref_nwumber=inv_id)
            VAT = (18/100)*(invoice.professional_amount)
            subtotal_pr = float(VAT+invoice.professional_amount)
            dis = Disbursements.objects.filter(invoice=invoice).all()
            for q in dis:
                subtotal_db +=float(q.disbursement_amount)
            grandtotal = subtotal_pr+subtotal_db
            #print(grandtotal) 
            context = {
                'object': invoice,
                'VAT':VAT,
                'subtotal_pr':subtotal_pr,
                'subtotal_db':subtotal_db,
                'grandtotal':grandtotal 
            }
            template = get_template('invoice/proformaInvoicePdf2.html')
            html = template.render(context)
            #css = ['firm/invoice/static/css/testing.css']
            pdf = pdfkit.from_string(html,False,configuration=_get_pdfkit_config(),options=wk_options)
            response = HttpResponse(pdf)
            response.headers['Content-Type']='application/pdf'
            #response.headers['Content-Disposition']='inline; filename=TaxInvoice'+str(pk)+'.pdf'
            #response = HttpResponse(pdf, content_type='application/pdf')
            return response
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have such an invoice")
            return redirect("/")
#using inlineformset_factory for the editing the user entries
class InvoiceDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	success_url = '/'
	model = Invoice
	def test_func(self):
		invoice = self.get_object()
		if self.request.user ==invoice.author:
			return True
		return False

