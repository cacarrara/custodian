# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext


def dashboard(request):
    context = {'title': 'Dashboard'}
    template = 'admin/dashboard.html'

    return render_to_response(template, context, 
        context_instance=RequestContext(request))