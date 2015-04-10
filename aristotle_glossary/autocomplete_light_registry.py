import autocomplete_light
import aristotle_glossary.models as G
import aristotle_mdr.autocomplete_light_registry as reg

autocompletesToRegister = [
        G.GlossaryItem,
    ]
for cls in autocompletesToRegister:
    # This will generate a PersonAutocomplete class
    x = reg.autocompleteTemplate.copy()
    x['name']='Autocomplete'+cls.__name__
    autocomplete_light.register(cls,reg.PermissionsAutocomplete,**x)
