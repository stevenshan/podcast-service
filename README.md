# podcast-service

Application for Capital One Software Engineering Summit (2018).

[http://podcast.stevenshan.com/](http://podcast.stevenshan.com/)

## Features
- Search for podcasts by keyword or by tag
- Several options for sorting podcasts or episodes:
    - for podcasts: most/least subscribers and lexicographic
    - for subscriptions: most/least subscribers, lexicographic, and frequency of new episode releases
        - prioritize listening to podcasts that release episodes more frequently because missing just a few days could put you far behind on new epsiodes
    - for episodes: chronological
- Several options for filtering podcasts or episodes such as setting minimum or maximum number of subscribers, and year episode was released
- Front page with most frequently searched queries and most popular podcasts for exploring new podcasts
- Mobile friendly page so you can use any device to view the web app

## Code Structure

I built the web app using Django. The project related code is in the `website` app. 

- The `website/views` module contains the Python backend that interacts with the gPodder API and processes the response to be rendered by the templates
    - `website/views/api.py` contains the interface for making API requests, a simple database interface for keeping key-value pairs from podcast names to URLs, and various helper functions.
    - `website/views/base.py` imports all of the modules needed to create a View
    - `website/views/__init__.py` imports all of the views that are referenced in `website/urls.py` to create each page of the website
    - the other Python files are Views corresponding to different pages of the website
- The `website/templates` and `website/static` directories contain the templates and the associated formatting

## Challenges
- the data from the gPodder API is occassionally outdated or has diverged from the RSS feed of the podcast so instead of using the Episode Data endpoint I scraped all of the data directly from the RSS feed
- this was my first time using Django so there's probably areas where the code was more complicated than it needed to be
- I wasn't sure how gPodder was mapping podcast names to URLs since many podcasts share a name and they did not assign a primary key to each podcast. My solution to this was to add podcasts as they were being searched to a dictionary along with the last segment of the `mygpo_link`, which served as the key.
- in some of the RSS feeds, episode's descriptions were stored in an XML `description` tag while other times they were in a `summary` tag under the `itunes` namespace

## Problem Statement
We live in the age of the podcast. It seems like almost everyone has one, with focuses ranging from broad news coverage to specific niche topics, with some podcasts being about nothing other than goofing off with friends. That podcast proliferation makes it difficult to keep up with what's new and interesting in the podcast world.

We want you to use gpodder.net API, plus any other public APIs you need, to build a deployable web app that will allow users to search, track, and recommend podcasts. 

Access the gpodder.net API here. Note: The Episode Data endpoint documentation is inaccurate - use podcast and url in place of podcast-url and episode-url respectively.

To solve this challenge, build a web application that provides:

- Data Visuals: Display the podcasts returned via search function, as well as key information about each podcast returned. Similarly, display the podcasts a user is subscribed to, as well as information that user might want to know at a glance about the subscriptions.
- Smart Searching: Give users the ability to search for podcasts by genre and by popularity.
- Smart Sorting: Based on how frequently each subscribed podcast has new episodes, which subscribed podcasts should the user listen to first in order to avoid falling behind? Assume the user is subscribed to the top 25 podcasts.

(Optional) Bonus features you may want to include:

- The ability to see podcasts that have gained the most subscribers in a given period of time.
- Recommendations within a genre.
- Recommendations based on similarity to a user's subscriptions.
- Generate a sample user's listening habits and subscriptions. How often 
would the user run out of podcasts to listen to? Which action would you take in response to that conclusion?
- Whatever interesting and helpful features you can come up with!
