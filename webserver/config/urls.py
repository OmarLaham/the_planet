# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf import settings
from django.conf.urls import url
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
#from rest_framework.authtoken.views import obtain_auth_token
from planet import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path('human/', include("apps.authentication.urls")), # Auth routes - login / register
    path('i18n/', include('django.conf.urls.i18n')), #https://docs.djangoproject.com/en/dev/topics/i18n/translation/#the-set-language-redirect-view
    path("", views.HomepageView.as_view(), name='home'),
    path("/", views.HomepageView.as_view(), name='home'),
    path("about", views.AboutThePlanetView.as_view(), name='about'),
    path("esperanto", views.HomepageView.as_view(), name='esperanto'),
    path("problems", views.ProblemsView.as_view(), name='problems'),
    path("teams", views.HomepageView.as_view(), name='teams'),
    path("support", views.HomepageView.as_view(), name='support'),
    path("esperanto", views.HomepageView.as_view(), name='profile'),
    path("id-card", views.HomepageView.as_view(), name='card'),
    path("problem-create", views.ProblemCreateView),
    path("problem-solve/<int:problem_id>", views.ProblemSubmitSolutionView.as_view()),
    path("problem-solution-evaluate/<int:solution_id>", views.ProblemSolutionEvaluation.as_view()),
    path("problem-rate", views.SolutionRatingAjax)
    # UI Kits Html files
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

