from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from datetime import datetime,date
from django.utils import timezone
class receipts(models.Model):
    receipt_number = models.CharField(max_length=20)
    date_created = models.DateTimeField(default=timezone.now)
    received_from = models.CharField(max_length=100)
    sum_in_words= models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    cash_cheque = models.CharField(max_length=50)
    balance = models.CharField(max_length=20)
    amount = models.CharField(max_length=100)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    def get_last_id():

        qry = receipts.objects.order_by(receipts.id.desc()).first()
        x = qry.id
        ym = date.today().strftime("%y%m")
        q_custom_id = "" + ym + str(x).zfill(3) + ""

        return q_custom_id

    def __str__(self):
        return self.received_from

    def get_absolute_url(self):
        return reverse("receipt-details",kwargs={"pk":self.pk})

    def get_absolute_url(self):
        return reverse("invoice_pdf",kwargs={"pk":self.pk})

