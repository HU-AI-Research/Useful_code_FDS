import json
import pandas as pd
from global_functions import extract_hashtags
from global_functions import open_file

def clean(word):
    new_word = word.upper()
    new_word = new_word.replace(".", "")
    new_word = new_word.replace(",", "")
    new_word = new_word.replace("!", "")
    new_word = new_word.replace("?", "")
    new_word = new_word.replace(":", "")
    new_word = new_word.replace(")", "")
    new_word = new_word.replace("'", "")
    new_word = new_word.replace('"', '')
    return new_word

tweets = open_file('Dashboard klimaat/#klimaat_combined_tweets.json')

df = pd.DataFrame(columns=['hashtag', 'user'])

for tweet in tweets:
    if ('RT @' not in tweet['tweet']):
        user = tweet['user']
        text = tweet['tweet']
        hashtags = extract_hashtags(text)
        for hashtag in hashtags:
            new_hashtag = clean(hashtag)
            new_row = {'hashtag': new_hashtag, 'user': user}
            df = df.append(new_row, ignore_index=True)

df_hashtag_count = df.groupby('hashtag')['hashtag'].count().reset_index(name="total")
df_hashtag_count = df_hashtag_count.sort_values(by="total", ascending=False).reset_index()
df_hashtag_count = df_hashtag_count.drop(columns=['index'])
df_hashtag_count.drop(df_hashtag_count[df_hashtag_count['hashtag'] == '#KLIMAAT'].index, inplace = True)
df_hashtag_count.drop(df_hashtag_count[df_hashtag_count['total'] < 2].index, inplace = True)

df_hashtag_count.to_csv(r'Dashboard klimaat/df_all_klimaat_extracted_hashtags.csv')

print(df_hashtag_count.head(15))