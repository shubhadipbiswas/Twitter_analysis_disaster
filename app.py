from attr import has
import streamlit as st
import matplotlib.pyplot as plt
from sentiment import preprocessing_data, graph_sentiment, analyse_mention, analyse_hashtag, download_data, gen_wordcloud, gen_poswordcloud, gen_neuwordcloud, gen_negwordcloud, subjectivity, countvector
import matplotlib.pyplot as plt

def plot_sentiment(analysis_counts):
    colors = analysis_counts.index.map({"Positive": "green", "Negative": "red", "Neutral": "yellow"})
    plt.figure(figsize=(8, 4))
    plt.bar(analysis_counts.index, analysis_counts['Counts'], color=colors)
    plt.xlabel('Sentiment')
    plt.ylabel('Counts')
    plt.title('Twitter Sentiment Analysis')
    return plt

st.set_page_config(
    page_title="Twitter Sentiment Analysis",
    page_icon="🕸",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Twitter Sentiment Analysis POC for Disaster Management")
st.markdown("*Developed on 10-11-2023 for POC (SB)*")

uploaded_file = st.sidebar.file_uploader("Upload a TSV file", type="tsv")
number_of_tweets = st.sidebar.number_input('How many tweets do you want to analyze?', min_value=100, max_value=10000, value=1000)

if uploaded_file is not None and st.sidebar.button('Analyze Tweets'):
    # Read and preprocess the uploaded file
    data = preprocessing_data(uploaded_file, number_of_tweets)
    analyse = graph_sentiment(data)
    mention = analyse_mention(data)
    hashtag = analyse_hashtag(data)
    img = gen_wordcloud(data)
    img1 = gen_poswordcloud(data)
    img2 = gen_neuwordcloud(data)
    img3 = gen_negwordcloud(data)
    subject = subjectivity(data)
    countdf = countvector(data)

    st.write(" ")
    st.header("Extracted and Preprocessed Tweets")
    st.write(data)
    download_data(data, label="twitter_sentiment_filtered")
    st.write(" ")
    st.subheader("Twitter Sentiment Analysis")
    plt = plot_sentiment(analyse)
    st.pyplot(plt)

    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("### Exploratory data analysis on the Tweets")

    col1, col2 = st.columns(2)
    with col1:
        st.text("Top 10 Hashtags used in {} tweets".format(number_of_tweets))
        st.bar_chart(hashtag)
    with col2:
        st.text("Most used words in the Tweets")
        st.bar_chart(countdf[1:11])

    col3, col4 = st.columns([1.5, 1])
    with col3:
        st.text("Wordcloud for {} tweets".format(number_of_tweets))
        st.image(img)
    with col4:
        st.text("Top 10 @Mentions in {} tweets".format(number_of_tweets))
        st.bar_chart(mention)
    
    col5, col6, col7 = st.columns(3)
    with col5:
        st.text("Wordcloud for Positive tweets")
        st.image(img1)
    with col6:
        st.text("Wordcloud for Neutral tweets")
        st.image(img2)
    with col7:
        st.text("Wordcloud for Negative tweets")
        st.image(img3)
    
    
