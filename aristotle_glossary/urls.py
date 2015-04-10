from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from aristotle_glossary import views
from aristotle_glossary import api

from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(api.GlossaryListResource())

# Recommended to put this at "/glossary" when including these URLs
urlpatterns = patterns('aristotle_glossary.views',
    url(r'^/?$', views.glossary, name='glossary'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^search_dialog/?$',  views.glossary_search, name='glossary_search'),
    url(r'^about/(?P<template>.+)/?$', views.DynamicTemplateView.as_view(), name="about"),
)