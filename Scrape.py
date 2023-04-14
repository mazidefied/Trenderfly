import csv
import snscrape.modules.twitter as sntwitter
import re

# prompt user for search queries, year to search from, and number of tweets to scrape
search_terms = input("Enter search queries (comma-separated): ").split(",")
search_year = int(input("Enter year to search from: "))
num_tweets = int(input("Enter number of tweets to scrape: "))

# prompt user for filename
filename = input("Enter title for scraped data set: ")

# set up lists to store raw and cleaned tweets
raw_tweets_list = []
cleaned_tweets_list = []

# use snscrape to search for tweets
print("Searching for tweets...")
try:
    for search_term in search_terms:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_term} since:{search_year}-01-01 until:{search_year}-12-31').get_items()):
            if i >= num_tweets:
                break

            # store the raw tweet content
            raw_tweets_list.append([tweet.date.year, tweet.id, tweet.content, tweet.url, tweet.user.username, tweet.user.location, tweet.user.followersCount, tweet.user.friendsCount, tweet.user.verified, tweet.sourceLabel, tweet.likeCount, tweet.retweetCount, tweet.replyCount, tweet.lang])

            # clean the tweet content
            content = re.sub(r"http\S+", "", tweet.content) # remove URLs
            content = re.sub(r"RT\s@\S+", "", content) # remove retweets
            content = re.sub(r"#\S+", "", content) # remove hashtags
            content = re.sub(r"@\S+", "", content) # remove mentions
            content = re.sub(r"[^a-zA-Z0-9\s]", "", content) # remove special characters
            content = content.strip() # remove leading/trailing white space

            # store the cleaned tweet content
            cleaned_tweets_list.append([tweet.date.year, tweet.id, content, tweet.url, tweet.user.username, tweet.user.location, tweet.user.followersCount, tweet.user.friendsCount, tweet.user.verified, tweet.sourceLabel, tweet.likeCount, tweet.retweetCount, tweet.replyCount, tweet.lang])
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

# save the raw tweets to a CSV file
with open(f"{filename}_raw.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Year', 'ID', 'Content', 'URL', 'Username', 'Location', 'Followers', 'Following', 'Verified', 'Source', 'Likes', 'Retweets', 'Replies', 'Language Code'])  # header row
    writer.writerows(raw_tweets_list)

# save the cleaned tweets to a CSV file
with open(f"{filename}_cleaned.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Year', 'ID', 'Content', 'URL', 'Username', 'Location', 'Followers', 'Following', 'Verified', 'Source', 'Likes', 'Retweets', 'Replies', 'Language Code'])  # header row
    writer.writerows(cleaned_tweets_list)

# print a message indicating the number of tweets scraped and the filenames of the saved files
print(f"\nScraped {len(raw_tweets_list)} tweets.\nRaw tweets saved to {filename}_raw.csv\nCleaned tweets saved to {filename}_cleaned.csv")
