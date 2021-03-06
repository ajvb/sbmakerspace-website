from django.contrib.auth.models import User
from django import forms
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from sbmakerspace_app.models import *

class MailingForm(forms.Form):
    email   = forms.EmailField()

    class Meta:
        fields = ('email',)
