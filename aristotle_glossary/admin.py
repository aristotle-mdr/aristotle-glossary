from django.contrib import admin
from aristotle_mdr import admin as aristotle_admin # Must include 'admin' directly, otherwise causes issues.
import aristotle_glossary.models as G

class GlossaryAlternateDefinitionInline(admin.TabularInline):
    model = G.GlossaryAdditionalDefinition
    extra=0

class GlossaryItemAdmin(aristotle_admin.ConceptAdmin):
    model = G.GlossaryItem
    fieldsets = aristotle_admin.ConceptAdmin.fieldsets
    inlines = aristotle_admin.ConceptAdmin.inlines + [GlossaryAlternateDefinitionInline]

admin.site.register(G.GlossaryItem,GlossaryItemAdmin)