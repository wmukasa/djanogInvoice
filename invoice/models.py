from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from datetime import datetime,date
from django.utils import timezone

class Invoice(models.Model):
    ref_nwumber = models.CharField(max_length=20)
    name_to = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    address_to = models.CharField(max_length=200)

    telephone_to = models.CharField(max_length=200, null=True, blank=True)
    email_to = models.EmailField(max_length=254, null=True, blank=True)
    box_number_to = models.CharField(max_length=200, null=True, blank=True)
    terms = models.CharField(max_length=200, null=True, blank=True)

    issue_date = models.DateTimeField(default=timezone.now)
    #issue_date =models.DateField(default=datetime.now().date())
    #due_date =db.Column(db.Date,nullable=False)
    vat = models.CharField(max_length=200, null=True, blank=True)
    bank =models.CharField(max_length=200)
    bank_branch =models.CharField(max_length=200)
    swift_code =models.CharField(max_length=200)
    account_number =models.CharField(max_length=200)
    professional_amount =models.FloatField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = 'invoice'
    def get_last_id():

        qry = Invoice.objects.order_by(Invoice.id.desc()).first()
        x = qry.id
        ym = date.today().strftime("%y%m")
        q_custom_id = "" + ym + str(x).zfill(3) + ""

        return q_custom_id

    def __str__(self):
        return self.ref_nwumber

    def get_absolute_url(self):
        return reverse("invoice-details",kwargs={"pk":self.pk})


class InvoiceLineItem(models.Model): 
    prof_heading = models.CharField(max_length=255, null=False, blank=False)
    prof_sub1 = models.CharField(max_length=200, null=True, blank=True)
    prof_sub2 = models.CharField(max_length=200, null=True, blank=True)
    prof_sub3 = models.CharField(max_length=200, null=True, blank=True)
    prof_sub4 = models.CharField(max_length=200, null=True, blank=True)
    prof_sub5 = models.CharField(max_length=200, null=True, blank=True)
    invoice = models.ForeignKey('Invoice',
                                related_name='lineItem', on_delete=models.SET_NULL,blank=True,null=True)
    class Meta:
        db_table = 'lineItem'

    def __str__(self):
        return (str(self.invoice))
    def get_absolute_url(self):
        return reverse("invoice-details",kwargs={"pk":self.pk}) 

'''
class InvoiceLineItem(models.Model):

    prof_heading = models.CharField(max_length=200)
    prof_sub1 = models.CharField(max_length=200)
    prof_sub2 = models.CharField(max_length=200)
    prof_sub3 = models.CharField(max_length=200)
    prof_sub4 = models.CharField(max_length=200)
    prof_sub5 = models.CharField(max_length=200)

    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id', ondelete='SET NULL'), nullable=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
        # Relationship
    invoice = db.relationship(
        'Invoice',
        backref=db.backref('laps', lazy='dynamic', passive_deletes=True, collection_class=list)

    )
'''
class Disbursements(models.Model):
    disbursement_amount =models.CharField(max_length=200, null=False, blank=False)
    disb_heading = models.CharField(max_length=200, null=False, blank=False)
    disb_sub1 = models.CharField(max_length=200, null=True, blank=True)
    disb_sub2 = models.CharField(max_length=200, null=True, blank=True)
    disb_sub3 = models.CharField(max_length=200, null=True, blank=True)
    invoice = models.ForeignKey('Invoice',
                                related_name='disbursement', on_delete=models.SET_NULL,blank=True,null=True)
    class Meta:
        db_table = 'Disbursements'

    def __str__(self):
        return str(self.invoice)  




