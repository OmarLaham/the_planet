# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf import settings
from os import path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse, Http404
from django import template
from django.views import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import pandas as pd
import numpy as np
import math
import random

import re #regex
import json
import gzip
from glob import glob, escape

def util_get_numeric(string):
    value = None
    dtype = None

    try:
        value = int(string)
        dtype = "int"
        return value, dtype
    except:
        try:
            value = float(string)
            dtype = "float"
            return value, dtype
        except:
            return value, dtype

    return value, dtype

def util_get_valid_lang_or_404(lang):
    if lang not in ["en", "eo"]:
        raise Http404("Invalid selected interface language.")

class Homepage(View):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):

        context = {}
        context["i18n"] = "en"

        return render(request, self.template_name, context)

class I18nSwitch(View):

    def get(self, request, *args, **kwargs):

        context = {}
        lang = context["lang"]

        return render(request, self.template_name, context)


def HomeJSONView(request):

    context = {}
    return JsonResponse(context)


class MetadataView(View):
    template_name = 'metadata.html'

    def get(self, request, *args, **kwargs):

        context = {}

        return render(request, self.template_name, context)

#@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        html_template = loader.get_template( load_template )

        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('not_used/templates/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('not_used/templates/page-500.html')
        return HttpResponse(html_template.render(context, request))
