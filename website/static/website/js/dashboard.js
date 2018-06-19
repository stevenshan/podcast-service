/*
 * Javascript code for extra sorting options on dashboard page
 */

/*
 * Helpers
 */

// get html element attribute or default to 0
function getAttrFloat(elem, key)
{
    try { return parseInt(parseFloat(elem.attr(key)) * 10) }
    catch(e) { return 0; }
}

// sorting methods

// sort numbers high to low
function highFreq(a, b)
{
    return getAttrFloat(b, "freq") - getAttrFloat(a, "freq");
}

// sort numbers low to high
function lowFreq(a, b)
{
    return getAttrFloat(a, "freq") - getAttrFloat(b, "freq");
}

/*
 * Extra sort method called by search.js
 */

function extraSort(results, key)
{
    switch(key)
    {
        case "highFreq":
        {
            results.sort(highFreq);
            break;
        }
        case "lowFreq":
        {
            results.sort(lowFreq);
            break; 
        }
    }
}
