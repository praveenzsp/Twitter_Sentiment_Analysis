import re
import tweepy
from flask import Flask
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
from flask import *
from tkinter import *
import pyperclip as pc
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np


class TwitterClient:

    def __init__(self):

        # keys and tokens from the Twitter Dev Console
        consumer_key = 'gkUeGpIjqhQXRfkTQyyCyZref'
        consumer_secret = 'KHSpzv1PZRb4YsNbSxMDGEHrzbJdFU8ByMIliQQwdDL9UQsA2o'
        access_token = '1349676607863091202-U9UWiuemyYNcfu4DbKclFpF3q56mfA'
        access_token_secret = 'TlfeBPSdumrltUIiQHAsVBUxanfAIGYzZthUC3jDsihSm'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    @staticmethod
    def clean_tweet(tweet):
        # '''
        # Utility function to clean tweet text by removing links, special characters
        # using simple regex statements.
        # '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        # '''
        # Utility function to classify sentiment of passed tweet
        # using textblob's sentiment method
        # '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10000000):
        # '''
        # Main function to fetch tweets and parse them.
        # '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

    @staticmethod
    def plot(x, y, z):
        data = {'Positive': x, 'Negative': y, 'Neutral': z}
        a = list(data.keys())
        b = list(data.values())
        plt.bar(a, b, color='green', width=0.3)
        plt.title('Twitter Sentiment Analysis')
        plt.xlabel('Sentiment')
        plt.ylabel('Percentage of Sentiment')
        plt.show()

    # @staticmethod
    # def flask_method():
    #     application = Flask(__name__)
    #
    #     @app.route('/')
    #     def home():
    #         return render_template('index.html')
    #     application.run()


# defining main function
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # api.flask_method()
    positive_tweets = []
    negative_tweets = []
    # total_tweets=[]

    root = Tk()
    root.geometry('600x600')

    # submit button functionality method
    def submit_button():
        x = entry1.get()
        y = int(entry2.get())

        tweets = api.get_tweets(query=x, count=y)

        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        try:
            # percentage of positive tweets
            positive = 100 * len(ptweets) / len(tweets)
            # print("Positive tweets percentage: ", positive, '%')
            # picking negative tweets from tweets

            # percentage of negative tweets
            negative = 100 * len(ntweets) / len(tweets)
            # print("Negative tweets percentage: ", negative, '%')

            # percentage of neutral tweets
            neutral = 100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)
            # print("Neutral tweets percentage: ", neutral, '%')
        except ZeroDivisionError:
            print('No positive tweets')


        # plotting the percentages
        # api.plot(positive, negative, neutral)

        # printing some positive tweets
        # print("\n\nPositive tweets:")
        for tweet in ptweets:
            positive_tweets.append('🔦'+tweet['text'] + '\n\n')
        # print(*positive_tweets)

        # printing some negative tweets
        # print("\n\nNegative tweets:")
        for tweet in ntweets:
            negative_tweets.append('🔦'+tweet['text'] + '\n\n')
        # print(*negative_tweets)
        # Generate word cloud



        # plotting the percentages
        api.plot(positive, negative, neutral)


    # exit button functionality method
    def exit_button():
        root.destroy()

    # generate button functionality method
    def generate_button():
        t1.insert(END, 'http://127.0.0.1:5000/')

    # Define a function to plot word cloud
    def plot_cloud():
        my_list = positive_tweets + negative_tweets
        unique_string = " ".join(my_list)
        wordcloud = WordCloud(background_color='white', width=1000, max_font_size=256, random_state=42, max_words=2000, height=500,).generate(unique_string)
        # plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.title('Wordcloud')
        plt.show()
        plt.close()

    # copy button functionality method
    def copy_and_exit_button():
        pc.copy('http://127.0.0.1:5000/')
        exit_button()
        application = Flask(__name__)

        @application.route('/')
        def home():
            return render_template('index.html', positive=positive_tweets, negative=negative_tweets)

        application.run(debug=False)



    # input window design
    label1 = Label(root, text='Enter your query:', font=('Italic', 10))
    label1.grid(row=0, column=0, padx=10, pady=10)
    entry1 = Entry(root, width=30)
    entry1.grid(row=0, column=1, padx=10, pady=10)
    label2 = Label(root, text='Enter number of tweets to analyse:', font=('Bold', 10))
    label2.grid(row=1, column=0, padx=10, pady=10)
    entry2 = Entry(root, width=14)
    entry2.grid(row=1, column=1, padx=10, pady=10)
    Button(root, text='submit to show graph', command=submit_button).grid(row=2, column=1, padx=10, pady=10)
    # Button(root, text='exit', command=exit_button).place(relx=0.5, rely=0.5)
    # Button(root, text='show tweets', command=show_tweets_button).grid(row=2, column=1, padx=10, pady=10)
    label3 = Label(root, text='Open the below generated URL in browser to see tweets:')
    label3.grid(row=3, column=0,padx=10, pady=10)
    t1 = Text(root, width=30, height=1)
    t1.grid(row=3, column=1, padx=10, pady=10)
    Button(root, text='Generate URL', command=generate_button).grid(row=4, column=0,padx=10, pady=10)
    Button(root, text='Copy URL and exit', command=copy_and_exit_button).grid(row=4, column=1, padx=10, pady=10)
    Button(root, text='Generate wordcloud ', command=plot_cloud).grid(row=5, column=0, padx=10, pady=10)
    root.configure(bg='lightskyblue1')
    root.title('Input Window')
    root.attributes('-fullscreen', False)
    root.mainloop()




if __name__ == '__main__':
    # calling the main function
    main()