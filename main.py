import requests
from twilio.rest import Client
import creds

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TWILIO_SID = creds.TWILIO_SID
TWILIO_AUTH_TOKEN = creds.TWILIO_AUTH_TOKEN

STOCK_API_KEY = creds.STOCK_API_KEY
NEWS_API_KEY = creds.NEWS_API_KEY

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT,params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[1]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[2]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = (difference / float(yesterday_closing_price)) * 100

if abs(diff_percent) > 2:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params= news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [(f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. "
                           f"\nBrief: {article['description']}") for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_= "+15642161321",
            to= "+919752334143"
        )

