import aristotle_glossary.models as models
from aristotle_mdr.utils import url_slugify_concept
from tastypie import fields
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization
from tastypie.authentication import MultiAuthentication, BasicAuthentication, SessionAuthentication
from tastypie.resources import ModelResource

class MyAuthentication(SessionAuthentication):
    """
    Authenticates everyone if the request is GET otherwise performs
    ApiKeyAuthentication.
    """

    def is_authenticated(self, request, **kwargs):
        if request.method == 'GET':
            return True
        return super(MyAuthentication, self).is_authenticated(request, **kwargs)

class GlossaryListResource(ModelResource):
    url = fields.CharField(readonly=True)
    class Meta:
        queryset = models.GlossaryItem.objects.all()
        resource_name = 'glossarylist'
        fields = ['id','name','description','url']
        authorization = ReadOnlyAuthorization()
        #authentication = MultiAuthentication(BasicAuthentication(), SessionAuthentication())
        authentication = MyAuthentication()
        filtering = {
            'name': ('exact', 'startswith', 'contains',),
            'id': ('exact','in'),
        }

    def dehydrate_url(self,bundle):
        return url_slugify_concept(bundle.obj)

    def get_object_list(self, request):
        return self._meta.queryset.visible(request.user)