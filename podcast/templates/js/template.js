/* Javascript for generic page template */

$(function(){ // on page load

    /*
    -------------------------------------------
    Navigation Menu Setup
    -------------------------------------------
    */

    // display first three links by default
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

        // cancel progation to ignore click on element
        $("#settingsMenu #navMenuToggle").click(function(e){
            e.stopPropagation();
            if (!$("#settingsMenu #navMenu").hasClass("expanded"))
            {
                $("#settingsMenu #navMenu").addClass("expanded");
                $("#searchBar").addClass("minimized");

                // hide title
                $("body").addClass("hideTitle");
            }
        });

        // essentially event for losing "focus" on menu bar
        $("body").click(function(){
            if ($("#settingsMenu #navMenu").hasClass("expanded"))
            {
                $("#settingsMenu #navMenu").removeClass("expanded");
                $("#searchBar").removeClass("minimized");

                // unhide title
                $("body").removeClass("hideTitle");
            }
        });
    }

    /*
    -------------------------------------------
    Navigation menu maximization on mobile device
    -------------------------------------------
    */

    // maximize navigation menu
    $("#navMenuToggleView").click(function(){
        $("#settingsMenu").addClass("maximized");
    });

    // minimize navigation menu
    $("#navMenuClose").click(function(){
        $("#settingsMenu").removeClass("maximized");
    });

    /*
    -------------------------------------------
    Search bar focus events
    -------------------------------------------
    */

    var focusOutEvent = function() {
        $("header #searchBar").removeClass("focused");
        $("#searchBarToggleStatus").prop("checked", false);
    };

    $("header #searchInput")
        .focus(function(){ // on focus event
            $("header #searchBar").addClass("focused");
        })
        .focusout(function(){ // when focus leaves
            if ($(this).val() == "") // if search bar is empty
            {
                window.setTimeout(function() {
                    focusOutEvent();
                }, 100);
            }
        });

    $("#searchInput + label").click(function(){
        var input = $("header #searchInput");
        if ($("header #searchBar").hasClass("focused")) {
            input.val("");
            focusOutEvent();
        }
        else {
            input.focus();
        }
    });

    /*
    -------------------------------------------
    Sidebar Minimization
    -------------------------------------------
    */
    // open sidebar
    $("#menuSidebarToggle").click(function(){
        $("body").addClass("menuOpen");
    });

    // close sidebar
    $("#bgOverlay, #sidebarHead i").click(function(){
        $("body").removeClass("menuOpen");
    });

    /*
    -------------------------------------------
    Search bar minimization
    -------------------------------------------
    */

    // focus on search bar when maximizing search bar
    $("#searchBarToggle").click(function(e){
        window.setTimeout(function(){
            $("#searchInput").focus();
        }, 50);
    });

    /*
    -------------------------------------------
    Navigation Menu Full Screen Colors
    -------------------------------------------
    */

    var counter = 0;
    var limit = 5;
    $("#settingsMenu #navMenu li").each(function(){
        $(this).addClass("color" + (counter % limit + 1));
        counter += 1;
    });

    /*
    -------------------------------------------
    Show user settings menu
    -------------------------------------------
    */

    $("#userMenuButton").click(function(e){
        $("#userMenu").addClass("maximized");
        e.stopPropagation();
    });

    $("#userMenu").click(function(e){
        e.stopPropagation();
    });

    $("#userMenu, #userMenuButton").bind('touchstart mousedown', function(event) {
        event.stopPropagation();
    });

    $(document).bind('touchstart mousedown', function(event) {
        $("#userMenu").removeClass("maximized");
    });

});