from aristotle_mdr import models as MDR
from glossary_search import forms
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

def glossary(request):
    return render(request,"aristotle_glossary/glossary.html",
        {'terms':MDR.GlossaryItem.objects.visible(request.user).order_by('name').all()
        })

@permission_required('aristotle_mdr.user_is_editor')
def glossary_search(request):
    """This is a custom dialog for TinyMCE
    Use a view to make generating the form portions needed easier.
    """
    form = forms.GlossarySearchForm(user=request.user) # A form bound to the POST data
    return render(request,"aristotle_glossary/glossary_dialog.html",{'form':form})
