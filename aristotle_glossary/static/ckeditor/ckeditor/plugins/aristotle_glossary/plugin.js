console.log("loading aristotle glossary")
CKEDITOR.plugins.add( 'aristotle_glossary', {
    icons: 'glossary',
    init: function( editor ) {
        editor.addCommand( 'insertGlossary', new CKEDITOR.dialogCommand( 'glossaryListDialog' )

        /*{
            exec: function( editor ) {
                makeGlossaryItemDialog(editor)
            }
        }*/);
        editor.ui.addButton( 'Glossary', {
            label: 'Insert glossary item',
            command: 'insertGlossary',
        });
    }
});
var dialog = "XX";

CKEDITOR.dialog.add( 'glossaryListDialog', function( editor )
{
    if (dialog == "XX" ) {
        getGlossaryItemDialog()
    }

	return {
		title : 'Glossary search',
		minWidth : 400,
		minHeight : 200,
		contents :
		[
			{
				id : 'general',
				label : 'Settings',
				elements :
				[
                	{
                		type : 'html',
                		html : dialog,
                	},
				]
			}
		],
        onOk: function() {
            var g_id = $('#id_items').val()
            var link_text = $('#id_link').val();

            content = '<a class="aristotle_glossary" data-aristotle-glossary-id="'+g_id+'" href="/item/'+g_id+'">' + link_text + '</a>';
            editor.insertHtml( content,"unfiltered_html" );
        }
	};
});

function getGlossaryItemDialog () {
    if (dialog == "XX" ) {
        $.ajax({
            url:'/glossary/search_dialog/',
            async:   false
        })
        .done(function( data ) {
            dialog = $(data)

            dialog.find('input').addClass('cke_dialog_ui_input_text')
            dialog.find('label').addClass('cke_dialog_ui_labeled_label').css('display','block')

            dialog = dialog.html()
        });
    }
    return dialog;
}
getGlossaryItemDialog()