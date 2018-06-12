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
            }
        });

        // essentially event for losing "focus" on menu bar
        $("body").click(function(){
            if ($("#settingsMenu #navMenu").hasClass("expanded"))
            {
                $("#settingsMenu #navMenu").removeClass("expanded");
                $("#searchBar").removeClass("minimized");
            }
        });
    }

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

    var minimizeSidebar = function() {
        $("body").removeClass("menuOpen");
    };
    $("#bgOverlay, #sidebarHead i").click(minimizeSidebar);

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

});