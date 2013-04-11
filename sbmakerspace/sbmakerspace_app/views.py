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

from vars import mckey

global ms
ms = MailSnake(mckey)

def index(request):
    if request.method == 'POST': # If the form has been submitted...
        #If a user submitted to the Mailing List Form
        if 'mailinglist' in request.POST:
            mailing_list_form = MailingForm(request.POST)
            if mailing_list_form.is_valid(): # All validation rules pass
                ms_lists = ms.lists()['data'] #Get all of the MailChimp Lists
                list_to_us = ms_lists[0] #TODO: Delete this, uncomment below.
#            for list in lists:
#                if list['name'] == 'SyndicateProClosedBetaSignup'
#                    list_to_use = list
                # Process the data in form.cleaned_data
                messages.success(request, "Thank you for signing up!\nWe will contact you with more information soon!")
                ms.listSubscribe( #Subscribe the user to our mailing list
                    id = list_to_use['id'],
                    email_address = form.cleaned_data['email'],
                    update_existing = True,
                    double_optin = False,
                )
            #
            contact_us_form = ContactForm()
        #If a user submitted to the Contact Us Form
        elif 'contactus' in request.POST:
            contact_us_form = ContactForm(request.POST) # A form bound to the POST data
            if contact_us_form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                messages.success(request, "Thank you for contacting us!")
                emails = [settings.EMAIL_HOST_USER, 'avb.wkyhu@gmail.com']
                content = contact_us_form.cleaned_data['message'] + "\n\n" +\
                          "From: %s" % form.cleaned_data['name'] +\
                          "\n\n" + "Their Email: %s" % form.cleaned_data['email']
                send_mail('[SBMakerspace] :' + contact_us_form.cleaned_data['subject'],
                           content, settings.EMAIL_HOST_USER, emails, fail_silently=True)
            #
            mailing_list_form = MailingForm()
        #
        return redirect('landingpage')
    else:
        mailing_list_form = MailingForm()
        contact_us_form = ContactForm()
    return render(request, "index.html", locals())
