from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render, \
    redirect
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt

from sbmakerspace_app.models import *
from sbmakerspace_app.model_forms import *
from sbmakerspace_app.forms import *

from mailsnake import MailSnake

#from vars import mckey

global ms
#ms = MailSnake(mckey)

def index(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MailingForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            #ms_lists = ms.lists()['data'] #Get all of the MailChimp Lists
            #list_to_us = ms_lists[0] #TODO: Delete this, uncomment below.
#            for list in lists:
#                if list['name'] == 'SBMakerspaceWebSite'
#                    list_to_use = list
            # Process the data in form.cleaned_data
            messages.success(request, "Thank you for signing up!\nWe will contact you with more information soon!")
#            ms.listSubscribe( #Subscribe the user to our mailing list
#                id = list_to_use['id'],
#                email_address = form.cleaned_data['email'],
#                update_existing = True,
#                double_optin = False,
#            )
            return redirect('index')
    else:
        form = MailingForm() # An unbound form
    return render(request, "index.html", locals())
