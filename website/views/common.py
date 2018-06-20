import re # regex
from rake_nltk import Rake # for keyword extraction
import json

###########################################################
# Data extraction
###########################################################

# regex pattern to get name of podcast from url
podcastPat = re.compile("\/podcast\/([^\/]+)$") # matches exactly one level after podcast
podcastPatWhole = re.compile("\/podcast\/(.+)") # get everything after podcast
subscribePatWhole = re.compile("\/subscribe\/(.+)") # get everything after podcast
unsubscribePatWhole = re.compile("\/unsubscribe\/(.+)") # get everything after podcast
podcastPatBreak = re.compile("[^\/]+") # split by delimeter /

# regex pattern to get podcast feed url from gpodder html code
gPodderReverse = re.compile("<a href=\"([^\"]+)\" title=\"Feed\">")

###########################################################
# Shared Methods
###########################################################

# returns generic header containing user agent
def genHeader(request):
    header = {}
    try:
        # get user-agent
        userAgent = request.META['HTTP_USER_AGENT']
        header["User-Agent"] = userAgent
    except:
        pass
    return header

# get directory path from url
def readURL(url, pattern = podcastPatWhole):
    matches = pattern.findall(url)
    if matches == None or len(matches) != 1:
        return None

    match = podcastPatBreak.findall(matches[0])
    if len(match) != 0:
        return match
    return None

# returns a list of keyword phrases using Rake NLP
def keywords(text, phraseLen = 2):
    phrases = []
    try:
        ignore = "'()[]{}!@#$%^&*?><,.\";:|\\`~"
        r = Rake(max_length=phraseLen, punctuations=ignore)
        r.extract_keywords_from_text(text)
        phrases = r.get_ranked_phrases()[:20]
    except:
        pass
    return phrases
