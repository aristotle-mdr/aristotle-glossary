from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from aristotle_mdr import models as MDR
import reversion


class GlossaryItem(MDR.concept):
    template = "aristotle_glossary/concepts/glossaryItem.html"
    index = models.ManyToManyField(MDR._concept,blank=True,null=True,related_name="related_glossary_items")


@reversion.register()
class GlossaryAdditionalDefinition(MDR.aristotleComponent):
    glossaryItem = models.ForeignKey(GlossaryItem,related_name="alternate_definitions")
    registrationAuthority = models.ForeignKey(MDR.RegistrationAuthority)
    definition = models.TextField()
    @property
    def parentItem(self):
        return self.glossaryItem
    class Meta:
        unique_together = ('glossaryItem', 'registrationAuthority',)


@receiver(post_save)
def add_concepts_to_glossary_index(sender, instance, created, **kwargs):
    if not issubclass(sender, MDR._concept):
        return
    if 'data-aristotle_glossary_id' in instance.definition:
        glossary_id = 1 # TODO: write code to find the id of the glossary item being inserted
        try:
            g = GlossaryItem.objects.get(pk=glossary_id)
        except GlossaryItem.DoesNotExist:
            pass # there is no glossary with that ID
            #TODO: Perhaps pass a friendly message - https://docs.djangoproject.com/en/1.7/ref/contrib/messages/
