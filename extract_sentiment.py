import json
import pandas as pd

def open_file(filename):
    with open(filename) as json_file:
        return json.load(json_file)

tweets = open_file('Dashboard klimaat/#klimaat_combined_tweets.json')
words = open_file('Dashboard klimaat/all_assesssments.json')

# df_rated_tweets = pd.read_csv('Dashboard klimaat/df_rated_tweets.csv', index_col=0)
df_rated_tweets = pd.DataFrame(columns=['user', 'tweet', 'date', 'sentiment', 'RT'])


for tweet in tweets:
    sentiment = 0
    if ('RT @' in tweet['tweet']):
        RT = True
    else:
        RT = False
    user = tweet['user']
    text = tweet['tweet']
    date = tweet['date']
    for word in text.split():
        word = word.lower()
        word = word.replace(",", "")
        word = word.replace(".", "")
        word = word.replace(":", "")
        word = word.replace("?", "")
        word = word.replace("#", "")
        word = word.replace("(", "")
        word = word.replace(")", "")
        word = word.replace("!", "")
        word = word.replace("'", "")
        word = word.replace(";", "")
        word = word.replace("&", "")

        for index, w in words['word'].items():
            if w == word:
                sentiment1 = words['evaluation1'][index]
                sentiment2 = words['evaluation2'][index]
                if sentiment1 == '++':
                    sentiment1 = 2
                elif sentiment1 == '+':
                    sentiment1 = 1
                elif sentiment1 == '0':
                    sentiment1 = 0
                elif sentiment1 == '-':
                    sentiment1 = -1
                elif sentiment1 == '--':
                    sentiment1 = -2
                else:
                    sentiment1 = 'no'

                if sentiment2 == '++':
                    sentiment2 = 2
                elif sentiment2 == '+':
                    sentiment2 = 1
                elif sentiment2 == '0':
                    sentiment2 = 0
                elif sentiment2 == '-':
                    sentiment2 = 1
                elif sentiment2 == '--':
                    sentiment2 = 2
                else:
                    sentiment2 = 'no'
                
                if sentiment2 == 'no' and sentiment1 == 'no':
                    sentiment = sentiment
                elif sentiment2 == 'no' and sentiment1 != 'no':
                    sentiment = sentiment + sentiment1
                elif sentiment2 != 'no' and sentiment1 == 'no':
                    sentiment = sentiment + sentiment2
                else:
                    sentiment = sentiment + ((sentiment1 + sentiment2)/2)
            

    new_row = {'user': user, 'tweet': text, 'date': date, 'sentiment': sentiment, 'RT': RT}
    df_rated_tweets = df_rated_tweets.append(new_row, ignore_index=True)

df_rated_tweets.to_csv(r'Dashboard klimaat/df_all_rated_tweets.csv')


print(df_rated_tweets.info)