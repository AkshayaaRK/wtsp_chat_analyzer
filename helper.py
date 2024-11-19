from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


def fetch_stats(user, df):
    if user != 'overall':
        df = df[df["users"] == user]

    num_messages = df.shape[0]
    words = []
    for i in df['messages']:
        words.extend(i.split())

    # media
    num_media = df[df['messages'] == "media"].shape[0]
    # link
    extract = URLExtract()
    links = []
    for i in df['messages']:
        links.extend(extract.find_urls(i))

    # return
    return num_messages, len(words), num_media, len(links)


def fetch_busy(df):
    y = df[df['users'] != 'notification']
    x = y['users'].value_counts()
    z = round(y['users'].value_counts() / df.shape[0], 2).reset_index().rename(columns={'count': 'percent'})
    z['percent'] = z['percent'].astype(str) + '%'
    x.head()

    return x, z


def word_cloud(user, df):
    if user != 'overall':
        df = df[df['users'] == user]

    f = open(r"C:\Users\R.K.Akshaya\Downloads\stop_hinglish.txt", "r")
    stop_words = f.read()

    temp = df[df['users'] != 'notification']
    temp = temp[temp['messages'] != 'media']

    def remove(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    # if df.empty or df['messages'].isna().all():
    # print(f"No messages available for user: {user}")
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    temp['messages'] = temp['messages'].apply(remove)
    df_wc = wc.generate(df['messages'].str.cat(sep=' '))
    return df_wc


def common_words(user, df):
    if user != 'overall':
        df = df[df['users'] == user]

    temp = df[df['users'] != 'notification']
    temp = temp[temp['messages'] != 'media']

    words = []
    f = open(r"C:\Users\R.K.Akshaya\Downloads\stop_hinglish.txt", "r")
    stop_words = f.read()
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    a = pd.DataFrame(Counter(words).most_common(20))
    return a


def emoji_tracker(user, df):
    if user != 'overall':
        df = df[df['users'] == user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    df = pd.DataFrame(Counter(emojis).most_common(10))
    return df


def m_timeline(user, df):
    if user != 'overall':
        df = df[df['users'] == user]

    timeline = df.groupby(['year', 'month_num','month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(user,df):
    if user != 'overall':
        df = df[df['users'] == user]
    df['daily_date']=df['date'].dt.date
    daily=df.groupby(df['daily_date']).count()['messages'].reset_index()
    return daily

def week_activity(user,df):
    if user != 'overall':
        df = df[df['users'] == user]

    return df['day_name'].value_counts()
def month_activity(user,df):
    if user != 'overall':
        df = df[df['users'] == user]

    return df['month'].value_counts()

def heat_map(user,df):
    if user != 'overall':
        df = df[df['users'] == user]

    period=[]
    for hour in df['hour']:
        if hour>12 and hour<24:
            period.append(str(hour-12)+"-"+str((hour-12)+1)+"pm")
        elif hour==0:
            period.append(str('00')+"-"+str(hour+1)+"am")
        elif hour==24:
            period.append(str(hour-12)+"-"+str(1)+"am")
        elif hour == 12:
            period.append(str(12) + "-" + str(1) +"pm")

        else:
            period.append(str(hour)+"-"+str(hour+1)+"am")
    df['period']=period
    period_order = [f"{i}-{i+1}am" for i in range(12)] + [f"{i}-{i+1}pm" for i in range(12, 24)]
    df['period'] = pd.Categorical(df['period'], categories=period_order, ordered=True)

    heat=df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)
    heat = heat[sorted(heat.columns)]
    return heat