from aristotle_mdr.forms.creation_wizards import UserAwareForm

from django import forms
from django.utils.translation import ugettext_lazy as _

from aristotle_glossary.models import GlossaryItem
from aristotle_mdr.contrib.autocomplete import widgets

"""
Technically not a real form, but a massive convenience for the glossary item TinyMCE bit
Never saves.
"""
class GlossarySearchForm(UserAwareForm):
    items = forms.ModelChoiceField(
                queryset=GlossaryItem.objects.all(),
                label=_("Glossary Item"),
                widget=widgets.ConceptAutocompleteSelect(
                    model=GlossaryItem
                )
            )
    link  = forms.CharField(required=False,label=_('Link text'))
