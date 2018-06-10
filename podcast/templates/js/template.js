/* Javascript for generic page template */

$(function(){ // on page load

    /*
    -------------------------------------------
    Search bar events
    -------------------------------------------
    */

    // elem parameter is #searchInput object
    var focusOutEvent = function(elem) {
        elem.removeClass("focused");
    };
    $("#searchInput")
        .focus(function(){ // on focus event
            $(this).addClass("focused");
        })
        .focusout(function(){ // when focus leaves
            if ($(this).val() == "") // if search bar is empty
            {
                focusOutEvent($(this));
            }
        });

    $("#searchInput + label").click(function(){
        var input = $("#searchInput");
        if (input.hasClass("focused")) {
            input.val("");
            focusOutEvent(input);
        }
        else {
            input.focus();
        }
    });

});