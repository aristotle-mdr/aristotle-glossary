from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from aristotle_mdr.utils import url_slugify_concept
from aristotle_glossary import models, forms

def glossary(request):
    return render(request,"aristotle_glossary/glossary.html",
        {'terms':models.GlossaryItem.objects.visible(request.user).order_by('name').all()
        })

@permission_required('aristotle_mdr.user_is_editor')
def search_dialog(request):
    """This is a custom dialog for TinyMCE
    Use a view to make generating the form portions needed easier.
    """
    form = forms.GlossarySearchForm(user=request.user) # A form bound to the POST data
    return render(request,"aristotle_glossary/glossary_dialog.html",{'form':form})

class DynamicTemplateView(TemplateView):
    def get_template_names(self):
        return ['aristotle_glossary/static/%s.html' % self.kwargs['template']]

def json_list(request):
    item_ids = []
    for iid in request.GET.getlist('items'):
        try:
            iid = int(iid)
            item_ids.append(iid)
        except:
            return JsonResponse({"error": "Glossary IDs must be integers"})
    items = [{'id':obj.id,'url':url_slugify_concept(obj),'name':obj.name,'definition':obj.definition}
        for obj in models.GlossaryItem.objects.visible(request.user).filter(id__in=item_ids)
    ]
    return JsonResponse({"items": items})