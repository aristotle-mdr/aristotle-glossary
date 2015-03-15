from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from aristotle_glossary import views

urlpatterns = patterns('aristotle_glossary.views',
    url(r'^glossary/?$', views.glossary, name='glossary'),
    url(r'^glossary/search_dialog/?$',  views.glossary_search, name='glossary_search'),
)