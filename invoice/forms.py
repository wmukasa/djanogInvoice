from django import forms
#from .models import receipts
from .models import Invoice
from datetime import datetime,date
from django.utils import timezone
#from django.forms import formset_factory
from django.forms import (formset_factory, modelformset_factory)
from .models import (Invoice,InvoiceLineItem,Disbursements)
#Use case 1: Create formset for a normal form

class invoiceCreateForm(forms.Form):

    prof_heading = forms.CharField(
        label='Professional Description',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter professional heading here'
        })
    )
    
    prof_sub1 = forms.CharField(
        label='subheading1',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter professional subheading1 here'
        })
    )
    
    prof_sub2 = forms.CharField(
        label=' subheading2',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter professional subheading2 here'
        })
    )
    
    prof_sub3 = forms.CharField(
        label=' subheading3',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter professional subheading3 here'
        })
    )
    prof_sub4 = forms.CharField(
        label=' subheading4',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter professional subheading4 here'
        })
    )
    prof_sub5 = forms.CharField(
        label='subheading5',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter professional heading5 here'
        })
    )
InvoiceFormset = formset_factory(invoiceCreateForm, extra=1)

class InvoiceSecondModelForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ('name_to','company_name','address_to','email_to','telephone_to','box_number_to',
                    'issue_date','terms','bank','bank_branch','swift_code','account_number','vat','professional_amount' )
        labels = {
            'name_to': 'name_to',
            'company_name':'company_name',
            'address_to':'address_to',
        }
        widgets = {
            'name_to': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the name to'
                }
            ),
            'company_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Incase of company enter'}
            ),
            'address_to': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the address'}
            ),
            'email_to': forms.TextInput(attrs={'class': 'form-control','placeholder': ''}
            ),
            'telephone_to': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the Telephone if any'}
            ),
            'box_number_to': forms.TextInput(attrs={'class': 'form-control','placeholder': ''}
            ),
            'issue_date': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Issue date'}
            ),
            'terms': forms.TextInput(attrs={'class': 'form-control','placeholder': ''}
            ),
            'bank': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the Bank name'}
            ),
            'bank_branch': forms.TextInput(attrs={'class': 'form-control','placeholder': ''}
            ),
            'swift_code': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the Swift Code'}
            ),
            'account_number': forms.TextInput(attrs={'class': 'form-control','placeholder': ''}
            ),
            'vat': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the Tax Invoice Number'}
            ),
            'professional_amount': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter the Professional Amount'}
            )
        }

    def __init__(self, *args, **kwargs):
        super(InvoiceSecondModelForm, self).__init__(*args, **kwargs)
        self.fields['vat'].required = False
        self.fields['company_name'].required = False
        self.fields['email_to'].required = False
        self.fields['telephone_to'].required = False
        self.fields['box_number_to'].required = False


'''
InvoiceSecondFormset = modelformset_factory(
    Invoice,
    fields=('name_to', ),
    extra=1,
    widgets={
        'name_to': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the Name of a company Or '
            }
        )
    }
)
'''
InvoiceLineItemModelFormset = modelformset_factory(
    InvoiceLineItem,
    fields=('prof_heading','prof_sub1','prof_sub2','prof_sub3','prof_sub4','prof_sub5', ),
    extra=1,

    widgets={'prof_heading': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the professional main heading'
        }),
        'prof_sub1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''
        }),
        'prof_sub2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''
        }),
        'prof_sub3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''
        }),
        'prof_sub4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''
        }),
        'prof_sub5': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''
        }),
    }
)


DisbursementsModelFormset = modelformset_factory(
    Disbursements,
    fields=('disbursement_amount','disb_heading','disb_sub1','disb_sub2','disb_sub3' ),
    extra=1,
    widgets={'disbursement_amount': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the Disbursement Amount'
        }),
        'disb_heading': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''
        }),
        'disb_sub1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''
        }),
        'disb_sub2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''
        }),
        'disb_sub3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''
        }),

    }
)

class InvoiceLineItemModelForm(forms.ModelForm):

    class Meta:
        # specify model to be used
        model = InvoiceLineItem
        fields = ['prof_heading','prof_sub1','prof_sub2','prof_sub3','prof_sub4','prof_sub5']