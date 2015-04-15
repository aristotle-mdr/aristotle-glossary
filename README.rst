Aristotle Glossary Extension
============================
The Aristotle Glossary Extension provides additional models for defining reusable
terms and a rich text plugins for inserting references into object definitions.

Screenshots
-----------

Quick start
-----------

1. Add "aristotle_glossary" to your INSTALLED_APPS setting like this::

        INSTALLED_APPS = (
            ...
            'haystack',
            'aristotle_mdr',
            'aristotle_glossary',
            ...
        )

#. Include the glssary URL definitions in your Django URLconf file. The glossary URLs
   Must exist at `/glossary/` for the glossary definition popovers to work.

        url(r'^glossary/', include('aristotle_glossary.urls')),

#. Include links in your HTML to ensure the javascript and CSS are loaded for the popovers.
   This can be done by creating a new local template for your project
   based on the `aristotle_mdr/scripts.py` template. More information on how to override files
   in in the `Aristotle Metadata Registry documentation on customisation<http://aristotle-metadata-registry.readthedocs.org/en/latest/installing/changing_styles.html#completely-overhauling-the-site>`_

        <script src="{% static 'aristotle_glossary/aristotle.glossary.js' %}" type="text/javascript"></script>
        <link rel="stylesheet" href="{% static 'aristotle_glossary/aristotle.glossary.css' %}" />

#. Update the ``CONTENT_EXTENSIONS`` list in the ``ARISTOTLE_SETTINGS`` dictionary in your ``settings.py`` file
   to let the registry know of the additional model. For example::

        ARISTOTLE_SETTINGS['CONTENT_EXTENSIONS'] = [
                'aristotle_glossary',
                # ... other models here based on your requirements
            ]

#. (Optional) Override the ``CKEDITOR_CONFIGS`` configuration dictionary to include a button
   in the rich text editor for in inserting links to glossary items. This can be done either
   by using the default Aristotle glossary configuration::

        from aristotle_glossary.settings import CKEDITOR_CONFIGS

   or manually by::

        CKEDITOR_CONFIGS = {
            'default': {
                'toolbar' : [
                        # ... other configuration options
                       { 'name': 'aristotletoolbar', 'items': [ 'Glossary' ] },
                ],
                'extraPlugins' : 'aristotle_glossary',
            },
        }

    Form more information on customising the CKeditor toolbar consult the
    `Django-CKEditor documentation<https://github.com/django-ckeditor/django-ckeditor>`_.

#. Run ``python manage.py migrate`` to update theyour database to include the models for the glossary.