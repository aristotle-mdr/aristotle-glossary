from django.conf.urls import include, url
from django.views.generic import TemplateView

from aristotle_glossary import views

# Recommended to put this at "/glossary" when including these URLs
urlpatterns = [
    url(r'^/?$', views.glossary, name='glossary'),
    url(r'^jsonlist/', views.json_list, name='json_list'),
    url(r'^search_dialog/?$',  views.search_dialog, name='search_dialog'),
    url(r'^about/(?P<template>.+)/?$', views.DynamicTemplateView.as_view(), name="about"),
]