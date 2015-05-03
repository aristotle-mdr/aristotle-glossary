from django.core.urlresolvers import reverse
from django.test import TestCase

import aristotle_mdr.models as models
import aristotle_mdr.tests.utils as utils
import aristotle_glossary.models as gmodels

from aristotle_mdr import perms
from aristotle_mdr.tests.test_admin_pages import AdminPageForConcept
from aristotle_mdr.tests.test_html_pages import LoggedInViewConceptPages
from django.test.utils import setup_test_environment
setup_test_environment()

class GlossaryPage(utils.LoggedInViewPages,TestCase):
    def test_logged_out_glossary_page(self):
        self.logout()
        response = self.client.get(reverse('aristotle_glossary:glossary',))
        self.assertEqual(response.status_code,200)
        for term in response.context['terms']:
            self.assertTrue(term.is_public)

#permissions test
class GlossaryVisibility(utils.ManagedObjectVisibility,TestCase):
    def setUp(self):
        super(GlossaryVisibility, self).setUp()
        self.item = models.GlossaryItem.objects.create(name="Test Glossary",
            workgroup=self.wg,
            )

class GlossaryItemAdminPage(AdminPageForConcept,TestCase):
    itemType=gmodels.GlossaryItem
    form_defaults={
        'alternate_definitions-TOTAL_FORMS':0,
        'alternate_definitions-INITIAL_FORMS':0,
        'alternate_definitions-MAX_NUM_FORMS':1,
        }

class CustomGlossaryDialogTests(utils.LoggedInViewPages,TestCase):
    """
    There isn't much we can do to test these yet, but we can verify they at least load.
    They are in the wizard section as they are used in the editing pages.
    """
    def test_glossary_search_dialog(self):
        self.logout()
        response = self.client.get(reverse('aristotle_glossary:search_dialog'))
        self.assertEqual(response.status_code,302) # redirect to login

        self.login_editor()
        response = self.client.get(reverse('aristotle_glossary:search_dialog'))
        self.assertEqual(response.status_code,200)

        response = self.client.post(reverse('aristotle_glossary:search_dialog'),{})
        self.assertEqual(response.status_code,200)


class GlossaryViewPage(LoggedInViewConceptPages,TestCase):
    url_name='glossary'
    itemType=gmodels.GlossaryItem

    def test_view_glossary(self):
        self.logout()
        response = self.client.get(reverse('aristotle_glossary:glossary'))
        self.assertTrue(response.status_code,200)

    def test_glossary_ajax_list(self):
        self.logout()
        import json
        gitem = gmodels.GlossaryItem(name="Glossary item",workgroup=self.wg1)
        response = self.client.get(reverse('aristotle_glossary:json_list')+'?items=%s'%gitem.id)
        data = json.loads(str(response.content))['items']
        self.assertEqual(data,[])

        gitem.readyToReview = True
        gitem.save()

        self.login_editor()

        self.assertTrue(perms.user_can_change_status(self.registrar,gitem))

        self.ra.register(gitem,models.STATES.standard,self.registrar)

        self.assertTrue(gitem.is_public())

        response = self.client.get(reverse('aristotle_glossary:json_list')+'?items=%s'%gitem.id)
        data = json.loads(str(response.content))['items']

        self.assertEqual(len(data),gmodels.GlossaryItem.objects.all().visible(self.editor).count())

        for i in gmodels.GlossaryItem.objects.filter(pk__in=[item['id'] for item in data]):
            self.assertEqual(i.can_view(self.editor),1)
