from django.core.urlresolvers import reverse
from django.test import TestCase

import datetime

import aristotle_mdr.models as models
import aristotle_mdr.tests.utils as utils
import aristotle_glossary.models as gmodels

from aristotle_mdr import perms
from aristotle_mdr.tests.main.test_admin_pages import AdminPageForConcept
from aristotle_mdr.tests.main.test_html_pages import LoggedInViewConceptPages
from django.test.utils import setup_test_environment
setup_test_environment()


def setUpModule():
    from django.core.management import call_command
    call_command('loadhelp', 'aristotle_help/concept_help/*', verbosity=0, interactive=False)


class GlossaryPage(utils.LoggedInViewPages,TestCase):
    def test_logged_out_glossary_page(self):
        self.logout()

        ra2 = models.RegistrationAuthority.objects.create(name="Test Glossary RA")
        self.wg2.registrationAuthorities.add(ra2)
        self.wg2.save()

        for i in range(5):
            gitem = gmodels.GlossaryItem.objects.create(name="Glossary item %s"%i,workgroup=self.wg2)

            models.Status.objects.create(
                concept=gitem,
                registrationAuthority=ra2,
                registrationDate=datetime.date(2000,1,1),
                state=self.ra.public_state,
                )
        gitem = gmodels.GlossaryItem.objects.create(name="Glossary item locked",workgroup=self.wg2)

        models.Status.objects.create(
            concept=gitem,
            registrationAuthority=ra2,
            registrationDate=datetime.date(2000,1,1),
            state=self.ra.locked_state,
            )
        gmodels.GlossaryItem.objects.create(name="Glossary item unregistered",workgroup=self.wg2)

        response = self.client.get(reverse('aristotle_glossary:glossary',))
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context['terms']),5)
        for term in response.context['terms']:
            self.assertTrue(term.is_public())
        self.assertTrue('Glossary item locked' not in response.content)
        self.assertTrue('Glossary item unregistered' not in response.content)

#permissions test
class GlossaryVisibility(utils.ManagedObjectVisibility,TestCase):
    def setUp(self):
        super(GlossaryVisibility, self).setUp()
        self.item = gmodels.GlossaryItem.objects.create(name="Test Glossary",
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

    def get_help_page(self):
        return reverse('aristotle_glossary:about',args=[self.item1._meta.model_name])

    def test_view_glossary(self):
        self.logout()
        response = self.client.get(reverse('aristotle_glossary:glossary'))
        self.assertTrue(response.status_code,200)

    def test_glossary_ajax_list_public(self):
        self.logout()
        import json
        gitem = gmodels.GlossaryItem.objects.create(name="Glossary item",workgroup=self.wg1)
        response = self.client.get(reverse('aristotle_glossary:json_list')+'?items=%s'%gitem.id)
        data = json.loads(str(response.content))['items']
        self.assertEqual(data,[])

        gitem.readyToReview = True

        self.assertTrue(perms.user_can_change_status(self.registrar,gitem))
        self.ra.register(gitem,models.STATES.standard,self.registrar)
        gitem = gmodels.GlossaryItem.objects.get(pk=gitem.pk)
        self.assertTrue(gitem.is_public())

        response = self.client.get(reverse('aristotle_glossary:json_list')+'?items=%s'%gitem.id)
        data = json.loads(str(response.content))['items']
        self.assertEqual(len(data),1)
        self.assertEqual(data[0]['id'],gitem.pk)


    def test_glossary_ajax_list_editor(self):
        self.login_editor()

        import json

        ra2 = models.RegistrationAuthority.objects.create(name="Test Glossary RA")
        self.wg2.registrationAuthorities.add(ra2)
        self.wg2.save()

        gitem = gmodels.GlossaryItem.objects.create(name="Glossary item",workgroup=self.wg2)
        response = self.client.get(reverse('aristotle_glossary:json_list')+'?items=%s'%gitem.id)
        data = json.loads(str(response.content))['items']
        self.assertEqual(len(data),0)

        s1 = models.Status.objects.create(
            concept=gitem,
            registrationAuthority=ra2,
            registrationDate=datetime.date(2000,1,1),
            state=self.ra.public_state,
            )

        gitem = gmodels.GlossaryItem.objects.get(pk=gitem.pk)
        self.assertTrue(gitem.is_public())

        response = self.client.get(reverse('aristotle_glossary:json_list')+'?items=%s'%gitem.id)
        data = json.loads(str(response.content))['items']

        self.assertEqual(len(data),1)

        for i in gmodels.GlossaryItem.objects.filter(pk__in=[item['id'] for item in data]):
            self.assertEqual(i.can_view(self.editor),True)

        response = self.client.get(reverse('aristotle_glossary:json_list')+'?items=%s&items=%s'%(gitem.id,self.item1.id))
        data = json.loads(str(response.content))['items']

        self.assertEqual(len(data),2)

        for i in gmodels.GlossaryItem.objects.filter(pk__in=[item['id'] for item in data]):
            self.assertEqual(i.can_view(self.editor),True)

    def test_malformed_glossary_ajax_list(self):
        self.logout()
        import json
        response = self.client.get(reverse('aristotle_glossary:json_list')+'?items=SELECT * FROM Users')
        data = json.loads(str(response.content))
        self.assertEqual(data.get('data',None),None)
        self.assertEqual(data['error'],"Glossary IDs must be integers")