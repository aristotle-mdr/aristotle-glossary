from django.contrib import admin
import aristotle_glossary.models as G
from aristotle_mdr.register import register_concept

class GlossaryAlternateDefinitionInline(admin.TabularInline):
    model = G.GlossaryAdditionalDefinition
    extra=0

register_concept(G.GlossaryItem,extra_inlines=[GlossaryAlternateDefinitionInline])
