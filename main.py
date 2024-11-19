import streamlit as st
import pre,helper
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
matplotlib.rcParams['font.family'] = 'Segoe UI Emoji'  # macOS


st.sidebar.title("whatsapp chat analyzer")
upload_file=st.sidebar.file_uploader("Choose a file")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")
    #st.text(data)
    df=pre.preprocess(data)

    user_list=df['users'].unique().tolist()
    user_list.remove('notification')
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user=st.sidebar.selectbox("show analysis wrt",user_list)
    if st.sidebar.button("show analysis"):
        st.title("Top Statistics")

        num_messages,words,num_media,links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            #st.metric(label='total messages',value=num_messages)
            st.header("total messages")
            st.title(num_messages)
        with col2:
            st.header("total words")
            st.title(words)
        with col3:
            st.header("media messages")
            st.title(num_media)
        with col4:
            st.header("total links")
            st.title(links)

        #monthlytimeline
        #st.dataframe(df)
        timeline=helper.m_timeline(selected_user,df)
        st.title("Timeline")
        if not timeline.empty and timeline['messages'].sum()>0:
            fig, axis = plt.subplots()
            axis.plot(timeline['time'],timeline['messages'],color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        else:
            st.header("No Data from this user")


        #daily timelinegit
        daily=helper.daily_timeline(selected_user,df)
        st.title("Daily Timeline")
        fig,ax=plt.subplots()
        ax.plot(daily['daily_date'],daily['messages'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #weekly activity
        st.title("Weekly Activity")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        #heatmap
        st.title("Weekly Activity Map")
        heatmap=helper.heat_map(selected_user,df)
        fig, ax = plt.subplots()
        ax=sns.heatmap(heatmap)
        st.pyplot(fig)

        #finding most active user
        if selected_user=='overall':
            st.title("most active users")
            x,z=helper.fetch_busy(df)
            fig,axis=plt.subplots()

            col1,col2=st.columns(2)

            with col1:
                axis.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(z)
                #st.dataframe(df)
#wordcloud
        st.title("Wordcloud")

        img=helper.word_cloud(selected_user,df)
        if img is None:
            st.write("No messages available for word cloud.")
        else:
            fig, axis = plt.subplots()
            axis.imshow(img)
            st.pyplot(fig)
#common words
        common_words=helper.common_words(selected_user,df)
        st.title("Most Used Words")
        if common_words.empty:
            st.header("No Messages By this User ")
        else:
            fig,axis=plt.subplots()
            axis.barh(common_words[0],common_words[1])
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
            st.dataframe(common_words)
#emoji
        emoji_trackers=helper.emoji_tracker(selected_user,df)
        st.title("Most Used Emojis")
        if not emoji_trackers.empty:


            col1,col2=st.columns(2)

            with col1:
                st.dataframe(emoji_trackers)

            with col2:
                fig,axis=plt.subplots()
                axis.pie(emoji_trackers[1],labels=emoji_trackers[0],autopct='%d%%',pctdistance=1.3)

                st.pyplot(fig)
        else:
            st.header("No emoji used")



