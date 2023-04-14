import csv

import snscrape.modules.twitter as sntwitter

import re

# prompt user for search queries and year to search from

search_terms = input("Enter search queries (comma-separated): ").split(",")

search_year = int(input("Enter year to search from: "))

# prompt user for filename

filename = input("Enter title for scraped data set: ")

# set up list to store cleaned tweets

tweets_list = []

# use snscrape to search for tweets

max_tweets = 2000  # limit to 2000 tweets

print("Searching for tweets...")

try:

    for search_term in search_terms:

        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_term} since:{search_year}-01-01 until:{search_year}-12-31').get_items()):

            if i >= max_tweets:

                break

            # clean the tweet content

            content = re.sub(r"http\S+", "", tweet.content) # remove URLs

            content = re.sub(r"RT\s@\S+", "", content) # remove retweets

            content = re.sub(r"#\S+", "", content) # remove hashtags

            content = re.sub(r"@\S+", "", content) # remove mentions

            content = re.sub(r"[^a-zA-Z0-9\s]", "", content) # remove special characters

            content = content.strip() # remove leading/trailing white space

            # get user location

            location = tweet.user.location if tweet.user.location else "Unknown"

            # get user follower count

            followers = tweet.user.followersCount if tweet.user.followersCount else 0

            # get user following count

            following = tweet.user.friendsCount if tweet.user.friendsCount else 0

            # check if user is verified

            verified = tweet.user.verified

            # get the source of the tweet

            tweets_source = tweet.sourceLabel if tweet.sourceLabel else "Unknown"

            tweets_list.append([tweet.date, tweet.id, content, tweet.url, tweet.user.username, location, followers, following, verified, tweets_source, tweet.likeCount, tweet.retweetCount, tweet.replyCount])

except Exception as e:

    print(f"An error occurred: {e}")

    exit()

# save the results to a CSV file

with open(f"{filename}.csv", mode='w', newline='', encoding='utf-8') as file:

    writer = csv.writer(file)

    writer.writerow(['Date', 'ID', 'Content', 'URL', 'Username', 'Location', 'Followers', 'Following', 'Verified', 'Source', 'Likes', 'Retweets', 'Replies'])  # header row

    writer.writerows(tweets_list)

# print the first 10 tweets

print("\nHere are the first 10 tweets:")

for tweet in tweets_list[:10]:

    print(f'{tweet[0]} - {tweet[1]} - {tweet[2]} - {tweet[3]} - {tweet[4]} - {tweet[5]} - {tweet[6]} followers - {tweet[7]} following - Verified: {tweet[8]}, Source: {tweet[9]}, {tweet[10]} likes - {tweet[11]} retweets - {tweet[12]} replies')

print(f"\nThank you for using my tool! Open {filename}.csv to view your scraped data.")

