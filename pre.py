import pandas as pd
import re

def preprocess(data):
    pattern = r'\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s?(?:AM|PM|am|pm|\u202Fpm|\u202Fam)\s-\s'
    messages = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)
    df = pd.DataFrame({'user_messages': messages, 'message_date': date})
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=False)
    try:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ', dayfirst=True)
    except ValueError:
        df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %I:%M %p - ", dayfirst=True)

    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split(r'^([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('notification')
            messages.append(entry[0])
    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_messages'], inplace=True)
    df.head()
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num']=df['date'].dt.month
    df['day_name'] = df["date"].dt.day_name()

    df['messages'] = df['messages'].str.replace("<Media omitted>\n", "media", regex=False)
    df['messages'] = df['messages'].str.replace("null\n", "call", regex=False)

    #df['messages'] = df['messages'].str.replace("<Media omitted>\n", "media", regex=False)

    return df