#-*- coding: utf-8 -*-

from django import template
import string
from collections import OrderedDict

register = template.Library()

@register.filter
def with_letter(terms):
    for t in terms:
        yield t, first_letter(t.name)

@register.filter
def first_letter(in_string):
    in_string = in_string.strip()
    if len(in_string) == 0:
        return 'symbols'
    letter = in_string[0]
    if not letter.isalpha():
        return 'symbols'
    return letter.lower()

@register.filter
def glossary_top_links(terms):

    letters = OrderedDict([('symbols','')]+[(s,'') for s in string.ascii_lowercase])

    for term in terms:
        f = first_letter(term.name)
        letters[f] = '#glossary_%s'%f
    return letters.items()
