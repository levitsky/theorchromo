import datetime

import django
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404

from theorchromo_online.forms import *
from theorchromo_online.computations import process_peptides

def index(request):
    output = {}
    if request.method == 'POST':
        chromoConditionsForm = ChromoConditionsForm(request.POST)
        peptideSequencesForm = PeptideSequencesForm(request.POST)
        if (chromoConditionsForm.is_valid() and
            peptideSequencesForm.is_valid()):
            cleaned_data = chromoConditionsForm.cleaned_data
            cleaned_data.update(peptideSequencesForm.cleaned_data)
            request.session['request_data'] = {}
            request.session['request_data'].update(cleaned_data)
            return HttpResponseRedirect('/results/')
    else:
        if request.session.has_key('request_data'):
            chromoConditionsForm = ChromoConditionsForm(
                request.session['request_data'])
            peptideSequencesForm = PeptideSequencesForm(
                request.session['request_data'])
        else:
            chromoConditionsForm = ChromoConditionsForm()
            peptideSequencesForm = PeptideSequencesForm()
    output['chromoConditionsForm'] = chromoConditionsForm
    output['peptideSequencesForm'] = peptideSequencesForm
    return render(request, 'index.html', output)

def help_page(request):
    return render_to_response('help.html')

def results(request):
    if request.session.has_key('request_data'):
        chromoConditionsForm = ChromoConditionsForm()
        request_data = [
            {'label' : field.label,
             'name'  : field.name,
             'value' : request.session['request_data'][field.name]}
            for field in chromoConditionsForm]
        processed_peptides = process_peptides(
            **request.session['request_data'])  
    return render_to_response('results.html', locals())
