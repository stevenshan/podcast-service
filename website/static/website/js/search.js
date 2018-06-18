/*
 * Javascript code for search results page
 */

/*
 * Helpers
 */

// get html element attribute or default to 0
function getAttr(elem, key)
{
    try { return parseInt(elem.attr(key)) }
    catch(e) { return 0; }
}

// get name of podcast in search result html element
function getTitleVal(elem)
{
    try { return elem.find(".title a").html().replace(/\s/g, ''); }
    catch(e) { return ""; }
}

// safely convert string to an integer or return null
function string2int(value)
{
    try 
    { 
        value = parseInt(value); 
        if (isNaN(value)) throw "bad string";
        return value;
    }
    catch(e) { return null; } 
}

// returns a function that checks if int falls between 
// minSubs and maxSubs for search results
function fallInRange()
{
    var min = string2int($("#minSubs").val());
    var max = string2int($("#maxSubs").val());
    if (min == null && max != null)
        return function(x){ return x <= max; }
    if (min != null && max == null)
        return function(x){ return x >= min; }
    if (min != null && max != null)
        return function(x){ return min <= x && x <= max; }
    return function(x){ return true; }
}

// sorting methods

// sort numbers high to low
function mostSubsSort(a, b)
{
    return getAttr(b, "subs") - getAttr(a, "subs");
}

// sort numbers low to high
function leastSubsSort(a, b)
{
    return getAttr(a, "subs") - getAttr(b, "subs");
}

// sort strings from a to z
function lexicAZ(a, b)
{
    var x = getTitleVal(a).toLowerCase();
    var y = getTitleVal(b).toLowerCase();
    if (x < y) return -1;
    if (x > y) return 1;
    return 0;
}

// sort strings from z to a
function lexicZA(a, b)
{
    return -1 * lexicAZ(a, b);
}

/*
 * Run function on load
 */

$(function(){

    /*
     * Sort search results
     */
     $("#searchSortOpt").change(function(){

        // get list of search results
        var results = [];
        $("#content .searchResult").each(function(){
            results.push($(this));
            $(this).remove();
        });

        // decide sort based on selection value
        switch ($(this).val())
        {
            case "mostSubscribers":
            {
                results.sort(mostSubsSort);
                break;
            } 
            case "leastSubscribers":
            {
                results.sort(leastSubsSort);
                break; 
            } 
            case "lexicAZ":
            {
                results.sort(lexicAZ);
                break; 
            } 
            case "lexicZA":
            {
                results.sort(lexicZA);
                break; 
            }
            default:
            {
                try
                {
                    extraSort(results, $(this).val());
                }
                catch(e) {}
            }
        }

        // add search results back to page
        for (var i = 0; i < results.length; i++)
        {
            $("#content").append(results[i]);

            // adjust odd parity to recolor results
            if (i % 2 == 0)
            {
                results[i].removeClass("odd");
            }
            else
            {
                results[i].addClass("odd");
            }
        }

    });

    /*
     * Events on limits on search for number of subscribers
     */

    function checkRange()
    {
        var checker = fallInRange();
        var visible = 0;
        $("#content .searchResult").each(function(){
            var subs = getAttr($(this), "subs");
            var display = "none";
            if (checker(subs))
            {
                display = "";
                visible += 1;
            }
            $(this).css("display", display);
        });

        // no search results in range
        // show suggestion to loosen range limitation
        if (visible == 0)
        {
            $("#filterTooWideMesg").css("display", "block");
        }
        else
        {
            $("#filterTooWideMesg").css("display", "");
        }
    }

    $("#minSubs").change(checkRange);
    $("#maxSubs").change(checkRange);

});

/* reset minimum and maximum subscriber filter */
function resetFilter()
{
    $("#minSubs").val("");
    $("#maxSubs").val("").trigger("change");
}