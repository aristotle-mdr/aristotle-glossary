CKEDITOR_CONFIGS = {
    'default': {
        #'toolbar': 'full',
        'toolbar' : [
            { 'name': 'clipboard', 'items': [ 'Cut', 'Copy', 'Paste', 'PasteText', '-', 'Undo', 'Redo' ] },
            { 'name': 'basicstyles', 'items' : [ 'Bold','Italic','Subscript','Superscript','-','RemoveFormat' ] },
            { 'name': 'links', 'items' : [ 'Link','Unlink' ] },
	        { 'name': 'paragraph', 'items' : [ 'NumberedList','BulletedList','-','Blockquote' ] },
    	    { 'name': 'insert', 'items' : [ 'Image','Table','HorizontalRule','SpecialChar'] },
            { 'name': 'aristotletoolbar', 'items': [ 'Glossary' ] },
            { 'name': 'document', 'items': [ 'Maximize','Source' ] },
        ],
        'extraPlugins' : 'aristotle_glossary',
    },
}