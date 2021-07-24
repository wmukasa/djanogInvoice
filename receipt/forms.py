from django import forms
from .models import receipts
from datetime import datetime,date
from django.utils import timezone


class receiptCreateForm(forms.Form):
    date_created = forms.DateField()
    #date_created = forms.CharField()
    #receipt_number = forms.CharField(widget=forms.TextInput(attrs={
        #'class':'textinput textInput form-control'
    #}))
    received_from =forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'receipt goes to',
        'class':'textinput textInput form-control'
    }))
    sum_in_words= forms.CharField(widget=forms.TextInput(attrs={
        'name':'sum_in_words',
        'required id':'sum_in_words',
        'placeholder':'amount of shillings in words',
        'class':'textinput textInput form-control'    
    }))
    reason = forms.CharField(widget=forms.TextInput(attrs={
        'name':'reason',
        'required id':'reason',
        'placeholder':'payment made for what reason',
        'class':'textinput textInput form-control'    
    }))
    cash_cheque = forms.CharField(widget=forms.TextInput(attrs={
        'name':'cash_cheque',
        'required id':'cash_cheque',
        'class':'textinput textInput form-control'    
    }))
    balance = forms.CharField(widget=forms.TextInput(attrs={
        'name':'balance',
        'required id':'balance',
        'class':'textinput textInput form-control'    
    }))
    amount = forms.CharField(widget=forms.TextInput(attrs={
        'name':'amount',
        'required id':'id_amount',
        'placeholder':'amount in figures',
        'class':'textinput textInput form-control'    
    }))
class receiptCreateModelForm(forms.ModelForm):
    date_created = forms.DateField()
    #date_created = forms.CharField()
    #receipt_number = forms.CharField(widget=forms.TextInput(attrs={
        #'class':'textinput textInput form-control'
    #}))
    received_from =forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'receipt goes to',
        'class':'textinput textInput form-control'
    }))
    sum_in_words= forms.CharField(widget=forms.TextInput(attrs={
        'name':'sum_in_words',
        'required id':'sum_in_words',
        'placeholder':'amount of shillings in words',
        'class':'textinput textInput form-control'    
    }))
    reason = forms.CharField(widget=forms.TextInput(attrs={
        'name':'reason',
        'required id':'reason',
        'placeholder':'payment made for what reason',
        'class':'textinput textInput form-control'    
    }))
    cash_cheque = forms.CharField(widget=forms.TextInput(attrs={
        'name':'cash_cheque',
        'required id':'cash_cheque',
        'class':'textinput textInput form-control'    
    }))
    balance = forms.CharField(widget=forms.TextInput(attrs={
        'name':'balance',
        'required id':'balance',
        'class':'textinput textInput form-control'    
    }))
    amount = forms.CharField(widget=forms.TextInput(attrs={
        'name':'amount',
        'required id':'id_amount',
        'placeholder':'amount in figures',
        'class':'textinput textInput form-control'    
    }))
    class Meta:
        # specify model to be used
        model = receipts
 
        # specify fields to be used
        fields = [
            "date_created",
            "received_from",
            "sum_in_words",
            "reason",
            "cash_cheque",
            "balance",
            "amount"]
