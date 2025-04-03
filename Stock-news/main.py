import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
api_key = "E5C53SUTKVVO9CB1"
API_KEY = "1c1d9afdd9a8446d9d1eed73972bc166"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters ={
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": api_key
}

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()
closing_data = data["Time Series (Daily)"]


#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
closing_price  = [value["4. close"] for value in closing_data.values()]
yesterday_closing = float(closing_price[0])


#TODO 2. - Get the day before yesterday's closing stock price
before_yesterday = float(closing_price[1])


#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(yesterday_closing-before_yesterday)
difference1 = yesterday_closing-before_yesterday
up_down = None
if difference1 > 0:
    up_down = "🔺"
else:
    up_down = "🔻"



#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage = round((difference/before_yesterday)*100)


#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if(percentage>5):
    print("Get News")

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
parameters1 ={
    "q": COMPANY_NAME,
    "apiKey": API_KEY
}

response1 = requests.get(NEWS_ENDPOINT, params=parameters1)
response1.raise_for_status()
data1 = response1.json()
article = data1["articles"]


#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
three_article = article[:3]

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

new_list = [f"{STOCK_NAME}: {up_down} {percentage} % \nHeadline: {item['title']}. \nBrief: {item['description']}" for item in three_article]


#TODO 9. - Send each article as a separate message via Twilio. 
def telegram_bot_sendtext(bot_message):
    
    bot_token = '8105276632:AAGqnqIHcAxJjVtqmX-ZwAXWLaQ8aIjGub4'
    bot_chatID = '6247095465'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


#Optional TODO: Format the message like this:

for item in new_list:
    telegram_bot_sendtext(item)

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

