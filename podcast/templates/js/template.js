/* Javascript for generic page template */

$(function(){ // on page load

    /*
    -------------------------------------------
    Navigation Menu Setup
    -------------------------------------------
    */

    if ($("#settingsMenu #navMenu li").length > 3)
    {
        var count = 0;
        $("#settingsMenu #navMenuToggle").css("display", "inline-block");
        $("#settingsMenu #navMenu li").each(function(){
            if (count < 3)
            {
                $(this).addClass("firstThree");
            }
            count += 1;
        });

        /* minimize menu if anything else is clicked */

        $("#settingsMenu #navMenuToggle").click(function(e){
            e.stopPropagation();
            if (!$("#settingsMenu #navMenu").hasClass("expanded"))
            {
                $("#settingsMenu #navMenu").addClass("expanded");
            }
        });

        $("body").click(function(){
            if ($("#settingsMenu #navMenu").hasClass("expanded"))
            {
                $("#settingsMenu #navMenu").removeClass("expanded");
            }
        });
    }

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
                var elem = this;
                window.setTimeout(function() {
                    focusOutEvent($(elem));
                }, 50);
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
            console.log("focus");
        }
    });

});