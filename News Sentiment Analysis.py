from newsapi import NewsApiClient
from textblob import TextBlob

newsapi = NewsApiClient(api_key="70f2acd1f6594ccd9b02d645aaa9280f")

articles = newsapi.get_everything(
q="Apple stock",
language="en"
)

scores=[]

for a in articles["articles"]:

    sentiment = TextBlob(a["title"]).sentiment.polarity

    scores.append(sentiment)

sentiment_score = sum(scores)/len(scores)

print("Market sentiment:", sentiment_score)

if sentiment_score > 0.2:
    signal = "BUY"

elif sentiment_score < -0.2:
    signal = "SELL"

else:
    signal = "HOLD"

print("Trading signal:", signal)