template_html = '<div class="popover" role="tooltip"><div class="arrow"></div><header class="popover-title"></header><div class="popover-content"></div></div>';

function itemFromId (msg,id) {
    var item = {name:'id: '+id,description:"error"}
    $.each(msg,function(i,glossary_item) {
        if (glossary_item.id == id) {
            item = glossary_item
        }
    })

    return item;
}

$(document).ready(function () {
    generateGlossaryPopovers();
});

function generateGlossaryPopovers() {
    var glossary_list = []
    $('[data-aristotle-glossary-id]').each(function(i){
        glossary_list.push($(this).data("aristotleGlossaryId"))
    })

    if (glossary_list != []) {
        suppressLoadingBlock = true;
        $.ajax({
          type: "GET",
          url: "/glossary/jsonlist/",
          data: { items: glossary_list, },
          traditional : true
        })
        .done(function( msg ) {
            glossary_list = msg.items
            suppressLoadingBlock = false;

            $('[data-aristotle-glossary-id]').each(function(i){
                item = itemFromId(glossary_list,$(this).data('aristotleGlossaryId'))
                $(this).addClass("glossary_link")
                    .attr('title','')
                    .popover({
                        trigger: "manual",
                        template:template_html,
                        title:item.name,
                        content:item.definition,
                        toggle:'popover',
                    }).on("mouseenter", function () {
                        var _this = this;
                        $(this).popover("show");
                        $(".popover").on("mouseleave", function () {
                            $(_this).popover('hide');
                        });
                    }).on("mouseleave", function () {
                        var _this = this;
                        setTimeout(function () {
                            if (!$(".popover:hover").length) {
                                $(_this).popover("hide");
                            }
                        }, 300);
                    });


          });
        })
    }
}