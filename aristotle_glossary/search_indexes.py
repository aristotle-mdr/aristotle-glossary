import models
from haystack import indexes
from aristotle_mdr.search_indexes import conceptIndex

class GlossaryItemIndex(conceptIndex, indexes.Indexable):
    def get_model(self):
        return models.GlossaryItem
