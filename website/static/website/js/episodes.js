/*
 * Javascript code for Podcast, Episode, and Episodes List pages
 * mainly for filtering or sorting episodes
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

/*
 * Run function on load
 */

$(function(){

    /*
     * Initialize filter by year parsing each episode's years
     */

    var years = []; 
    // get all the years that have episodes
    $("#podcastEpisodes .episodeSummary")
        .each(function(e){
            elem = $(this).find(".episodeRelease small");
            var date = new Date(Date.parse(elem.html()));
            var year = date.getFullYear();
            if (years.indexOf(year) == -1)
            {
                years.push(year);
            }
            $(this).attr("year", year);
        });

    // reverse order sort
    years.sort(function(a, b){ return b - a; });

    // add years to select option
    for (var i = 0; i < years.length; i++)
    {
        var year = years[i];
        $("#episodeYearRestrict")
            .append("<option value=\"" + year + "\">" + year + "</option>");
    }

    /*
     * Hide/Reveal episodes by year
     */

    $("#episodeYearRestrict").change(function(){
        var elem = $(this);
        if (elem.val() == "all")
        {
            $("#podcastEpisodes .episodeSummary").css("display", "");
        }
        else
        {
            $("#podcastEpisodes .episodeSummary").each(function(){
                var value = getAttr($(this), "year") == elem.val() ?
                        "" : "none";
                $(this).css("display", value);
            });
        }
    });

    /*
     * Sorting episodes by recency
     */

     /* event when user changes sorting option */
     $("#episodeSortOpt").change(function(){
        // get list of episodes
        var episodes = [];
        $("#podcastEpisodes .episodeSummary").each(function(){
            episodes.push($(this));
            $(this).remove();
        });

        var reverse = $(this).val() != "newest";

        // sort episodes based on user's choice
        episodes.sort(function(a, b){
            return (getAttr(a, "enum") - getAttr(b, "enum")) *
                    (reverse ? 1 : -1);
        });

        // add episodes back to pages
        for (var i = 0; i < episodes.length; i++)
        {
            $("#podcastEpisodes").append(episodes[i]);
        }

     });
});