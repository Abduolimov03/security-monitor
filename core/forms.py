from django import forms
from .models import DomainRecord

class DomainForm(forms.ModelForm):
    class Meta:
        model = DomainRecord
        fields = ['email', 'domain']
