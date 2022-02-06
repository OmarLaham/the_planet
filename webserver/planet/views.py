# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf import settings
from os import path
from django.urls import resolve
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse, Http404
from django import template
from django.views import View

from django.utils import translation
from django.utils.translation import gettext as _

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView, ListView, CreateView
from planet.users import models

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.decorators import method_decorator

import pandas as pd
import numpy as np
import math
import random

import re #regex
import json
import gzip
from glob import glob, escape

def is_content_manager(user):
    return user.groups.filter(name="ContentManager").exists()

def is_solution_evaluator(user):
    return user.groups.filter(name="SolutionEvaluator").exists()

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

def util_get_i18n_context(lang):
    context = {"i18n":lang}
    return context

def util_get_valid_lang_or_404(lang):
    if not lang or lang == "":
        return "en-us"#default is English
    if lang not in ["en-us", "eo"]:
        raise Http404("Invalid selected interface language: {0}.".format(lang))
    return lang

class HomepageView(View):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        util_get_valid_lang_or_404(request.LANGUAGE_CODE)
        context = {}#util_get_i18n_context(current_lang)

        return render(request, self.template_name, context)


class AboutThePlanetView(View):
    template_name = 'home/about_the_planet.html'

    def get(self, request, *args, **kwargs):
        util_get_valid_lang_or_404(request.LANGUAGE_CODE)

        context = {}  # util_get_i18n_context(current_lang)

        return render(request, self.template_name, context)

class ProblemsView(View):
    template_name = 'home/problems.html'

    def get(self, request, *args, **kwargs):
        util_get_valid_lang_or_404(request.LANGUAGE_CODE)

        context = {}  # util_get_i18n_context(current_lang)

        return render(request, self.template_name, context)

@user_passes_test(is_content_manager)
class ProblemCreateView(CreateView):
    model = models.Problem
    fields = ['title', 'body', 'category', 'prize', 'allow_attachment', 'deadline']


class ProblemSubmitSolutionView(View):#LoginRequiredMixin
    template_name = 'home/problem_solution_submit.html'

    def get(self, request, *args, **kwargs):
        util_get_valid_lang_or_404(request.LANGUAGE_CODE)

        context = {}  # util_get_i18n_context(current_lang)

        return render(request, self.template_name, context)

@login_required
def SolutionRatingAjax(request):

    current_lang = util_get_valid_lang_or_404(request.LANGUAGE_CODE)
    context = {}
    solution_id = request.kwargs["solution_id"]
    rating = request.kwargs["rating"]

    #TODO: compelete code

    return JsonResponse(context)

#@user_passes_test(is_solution_evaluator)#, login_url='/member/login')
class ProblemSolutionEvaluation(View):
    template_name = 'home/problem_solution_evaluation.html'

    def get(self, request, *args, **kwargs):
        util_get_valid_lang_or_404(request.LANGUAGE_CODE)

        context = {}  # util_get_i18n_context(current_lang)

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
