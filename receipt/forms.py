from django import forms
from .models import receipts
from datetime import datetime,date
from django.utils import timezone


class receiptCreateForm(forms.Form):
    date_created = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Date created',
        'class':'textinput textInput form-control'
    }))
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
class ReceiptCreat(forms.ModelForm):
    class Meta:
        model = receipts
        fields = ('date_created','received_from','sum_in_words','reason','cash_cheque','balance',
                    'amount' )
        labels = {
            'date_created': 'date_created',
            'received_from':'received_from',
            'sum_in_words':'sum_in_words',
        }
        widgets = {
            'date_created': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the date created'
                }
            ),
            'received_from': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Incase of received from'}
            ),
            'sum_in_words': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter sum in words'}
            ),
            'reason': forms.TextInput(attrs={'class': 'form-control','placeholder': ''}
            ),
            'cash_cheque': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the cash/cheque'}
            ),
            'balance': forms.TextInput(attrs={'class': 'form-control','placeholder': ''}
            ),
            'amount': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter amount'}
            )
        }