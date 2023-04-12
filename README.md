# twitch_social_link_tester

## What is this?
This is python script that checks outdated links on Twitch profiles.

## How does it work?
### Single profile mode
The script loads the webpage of the profile, waits for the panels to load and extracts all links.\
When the link contain Twitter, YouTube, Instagram, TikTok or Discord it will be tested.\
Then the script loads each of of those links, waits in some cases for it to load and checks them for keywords indicating an outdated profile on that url. This is currently not a very good method because a retweet of a deleted tweet can lead to the profile being marked as outdated.

### Category search mode
This loads the category link you provided and loads all twitch streams on the first page of the category url. Then it executes the same code for the "Single profile mode" for each found Twitch profile.\
There is currently no support for cookies, so either you specify to rank by lower view count to higher view count or get all popular streamers where it is unlikely to detect outdated links.

## Why?
I don't know. I don't like outdated links and I wanted to have a reason to interact with people.

## Why is the code so bad?
This is just a small project that I wanted to do and the core functionality was done in an afternoon without much experience in python or the libraries that this uses.
Maybe I will optimnize this code but I am busy studying so ¯\\\_(ツ)\_/¯\
If you want to contribute, I would be happy to see what you can add :)

## What libraries does this use?
- beautifulsoup
- selenium
- termcolor (not very necessary but looks good :D)
- some standard libraries (have a quick look at the top of the python script)
