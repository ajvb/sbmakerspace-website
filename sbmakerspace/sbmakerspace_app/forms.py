from django.contrib.auth.models import User
from django import forms
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from sbmakerspace_app.models import *

class ContactForm(forms.Form):
    name    = forms.CharField(max_length=40)
    email   = forms.EmailField()
    subject = forms.CharField(max_length=40)
    message = forms.CharField(widget=forms.Textarea)

class MailingForm(forms.Form):
    email   = forms.EmailField()
