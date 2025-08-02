import streamlit as st
import pandas as pd
import random

# Page configuration
st.set_page_config(page_title="Random Tweet Display", page_icon="🐦", layout="centered")
st.title("🐦 Random Tweet Display")

# Google Sheet ID and URL
sheet_id = "1cSUKodL-VbDtEpmpPnvtS8FAcKM72GHdpKAgyN3op_4"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# Load tweet data
@st.cache_data
def load_tweets(url):
    try:
        df = pd.read_csv(url)
        tweet_col = next((col for col in df.columns if 'tweet' in col.lower()), None)
        if tweet_col:
            df = df[df[tweet_col].notna() & (df[tweet_col] != '')]
            return df[tweet_col].tolist()
        else:
            st.error("No column with 'tweet' found.")
            return []
    except Exception as e:
        st.error(f"Error loading sheet: {e}")
        return []

tweets = load_tweets(csv_url)

if tweets:
    if "current_tweet" not in st.session_state:
        st.session_state.current_tweet = random.choice(tweets)

    st.subheader("Current Tweet")

    # Display tweet
    st.text_area("Tweet", value=st.session_state.current_tweet, height=150)

    # Buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 New Random Tweet"):
            st.session_state.current_tweet = random.choice(tweets)
            st.rerun()




else:
    st.error("No valid tweets found or failed to load sheet.")
 
