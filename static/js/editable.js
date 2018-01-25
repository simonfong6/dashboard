$(document).ready(function() {
    function toggle_edit(){
        state = $(this).parents(".card").attr("contenteditable");
        console.log(state);
        if(state == "False"){
            $(this).parents(".card").attr("contenteditable","True");
        }else{
            // Get this card
            var card = $(this).parents(".card");
            
            // Make not editable
            card.attr("contenteditable","False");
            
            // Get the card ID
            var id = card.attr("id");
            
            // Get card title
            var card_title = $(this).parents('.card-title');
            
            // Get card description
            var card_description = card_title.siblings('.card-text');
            
            // Get all the card links
            var card_links = card.find('.card-link');
            
            // Init empty array for links
            var card_links_objects = [];
            
            // Append all the links and titles to links array
            $.each(card_links, function(key, value){
                var link_title = $(value).text();
                var link_url = $(value).attr('href');
                
                var link_object = {
                    'link_title': link_title,
                    'link_url': link_url
                };
                
                card_links_objects.push(link_object);
            });
            
            var card_to_send = {
                'id': id,
                'card_title': card_title.text(),
                'card_description': card_description.text(),
                'card_links': card_links_objects
            }
            
            console.log(card_to_send);
            $.post("/bookmarks/update", JSON.stringify(card_to_send)).done(function( data ) {
                console.log(data);
            });
        }
    }
    console.log("ready!");
    $(".editable").click(toggle_edit);
});
