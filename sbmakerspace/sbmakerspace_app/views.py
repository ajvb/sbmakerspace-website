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
from sbmakerspace_app.forms import *

from mailsnake import MailSnake

from sbmakerspace.vars import mckey

global ms
ms = MailSnake(mckey)

def index(request):
    if request.method == 'POST': # If the form has been submitted...
        #If a user submitted to the Mailing List Form
        if 'volunteer' in request.POST:
            volunteer_mailing_list_form = MailingForm(request.POST, prefix="volunteer")
            if volunteer_mailing_list_form.is_valid(): # All validation rules pass
                ms_lists = ms.lists()['data'] #Get all of the MailChimp Lists
                for list in ms_lists:
                    if 'Volunteer' in list['name']:
                        list_to_use = list

                # Process the data in form.cleaned_data
                messages.success(request, "Thank you for signing up!\nWe will contact you with more information soon!")
                ms.listSubscribe( #Subscribe the user to our mailing list
                    id = list_to_use['id'],
                    email_address = volunteer_mailing_list_form.cleaned_data['email'],
                    update_existing = True,
                    double_optin = False,
                )
            classes_mailing_list_form = MailingForm(prefix="classes")
        elif 'classes' in request.POST:
            classes_mailing_list_form = MailingForm(request.POST, prefix="classes")
            if classes_mailing_list_form.is_valid(): # All validation rules pass
                ms_lists = ms.lists()['data'] #Get all of the MailChimp Lists
                for list in ms_lists:
                    if 'Classes' in list['name']:
                        list_to_use = list

                # Process the data in form.cleaned_data
                messages.success(request, "Thank you for signing up!\nWe will contact you with more information soon!")
                ms.listSubscribe( #Subscribe the user to our mailing list
                    id = list_to_use['id'],
                    email_address = classes_mailing_list_form.cleaned_data['email'],
                    update_existing = True,
                    double_optin = False,
                )
            volunteer_mailing_list_form = MailingForm(prefix="volunteer")
        return redirect('index')
    else: #At GET request, do the below.
        volunteer_mailing_list_form = MailingForm(prefix="volunteer")
        classes_mailing_list_form = MailingForm(prefix="classes")
    return render(request, "index.html", locals())
