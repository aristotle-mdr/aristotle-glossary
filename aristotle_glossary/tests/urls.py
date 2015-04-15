from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('aristotle_mdr.urls')),
    url(r'^glossary/', include('aristotle_glossary.urls',app_name="aristotle_glossary",namespace="glossary")),
    )