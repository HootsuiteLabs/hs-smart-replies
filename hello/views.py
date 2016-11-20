import json
import random
import requests

from django.shortcuts import render
from django.http import HttpResponse

THANK_YOU = [
  'Thank you very much!',
  'Awwwww, thank you :-) ',
  'Thanks!!! ',
  'That is very nice of you! '
]

SORRY = [
  'Sorry to hear that. ',
  'I am very sorry. ',
  'Oooops! Our bad. ',
  'Apologies. '
];

PROBLEM = [
  'Our support team is now aware of this issue. #stayTuned ',
  'We have filed a report in our system. Please stay tuned. ',
  'Our very smart engineers are working on this. Stay tuned! '
];

YOU_ARE_WELCOME = [
  'You are welcome! ',
  'Glad we could help! ',
  'My pleasure! '
]

CRITICISM = [
  'Thank you for your feedback, we are working hard to serve you better. ',
  'Loud and clear. We will try harder next time. ',
  'We appreciate your honesty. ',
  'We value your honest feedback. '
];

INTEREST = [
  "Let's connect, I can help you find what you are looking for. ",
  "I think I can help you with that! I'll DM you some details. ",
  "Our product may be the perfect fit for you. Let's connect! "
]

def randomizer(action):
  return random.choice(action)

def get_sentence(text, sentiment, intent, keyword):
  sentence = ''
  if intent == 'interest':
    return randomizer(INTEREST)
  if sentiment == 'negative':
    sentence = randomizer(SORRY)
  elif sentiment == 'positive':
    if 'thank' in text:
      return randomizer(YOU_ARE_WELCOME)
    elif intent == 'compliment':
      return randomizer(THANK_YOU)
  if intent == 'problem':
    return sentence + randomizer(PROBLEM)
  if intent == 'criticism':
    return sentence + randomizer(CRITICISM)
  if intent == 'how-to':
    return sentence + 'I will DM you some info to help you out with this!'
  return sentence

def get_sentiment(text):
    url = "https://gateway-a.watsonplatform.net/calls/text/TextGetTextSentiment"
    querystring = {
        "apikey": "3f2b08f9bf2c5f59a2d7b2d61dd95890a80fb2b6",
        "text": text,
        "outputMode": "json"}
    sentiment_analysis = requests.request("GET", url, params=querystring)
    print 'sentiment AJAX call!!!!!'
    print sentiment_analysis.json()
    return sentiment_analysis.json().get('docSentiment', {})

def get_keywords(text):
    url = "https://gateway-a.watsonplatform.net/calls/text/TextGetRankedKeywords"
    querystring = {
        "apikey": "3f2b08f9bf2c5f59a2d7b2d61dd95890a80fb2b6",
        "text": text,
        "outputMode": "json"}
    keywords = requests.request("GET", url, params=querystring)
    return keywords.json().get('keywords', [{'text': ''}])

def get_intent(text):
    url = "https://api.projectoxford.ai/luis/v2.0/apps/2e6694e2-a7bb-486f-b2eb-ec6df5ac5041"
    querystring = {
        "subscription-key": "d85f1326ee7f4935afc434db40db18b3",
        "q": text,
        "verbose": True}
    intent = requests.request("GET", url, params=querystring)
    return intent.json().get('topScoringIntent',{})

# AI API endpoint
def get_replies(request):
    text = request.GET.get('text','')
    sentiment = get_sentiment(text)
    print 'sentiment is!!!!!!!!!!'
    print sentiment
    top_scoring_intent = get_intent(text)
    keywords = get_keywords(text)
    response = {
        'originalText': text,
        'replies': [get_sentence(text, sentiment.get('type'), top_scoring_intent.get('intent'), keywords[0].get('text'))],
        'sentiment': sentiment,
        'keywords': keywords,
        'topScoringIntent': top_scoring_intent
    }
    return HttpResponse(json.dumps(response),
                            content_type="application/json");

# Main view
def index(request):
    return render(request, 'index.html')
