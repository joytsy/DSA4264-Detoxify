import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Analysis Overview")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Frequency Trend", "Topic Modeling", "Upload CSV"]
)

# Tab 1: Overview
with tab1:
    st.write("Overview of the classification results.")
    if "classified_df" in st.session_state:
        df = st.session_state.classified_df
        st.write("Summary of classified data:")
        st.dataframe(df.head())
    else:
        st.write("Please upload a CSV file in the 'Upload CSV' tab to start analysis.")

# Tab 2: Frequency Trend
with tab2:
    st.write("Frequency trend over the years.")
    if "classified_df" in st.session_state:
        df = st.session_state.classified_df
        if "year" in df.columns:
            trend_data = (
                df.groupby(["year", "classification"]).size().unstack(fill_value=0)
            )
            st.write("Frequency of classifications over the years:")
            fig, ax = plt.subplots()
            trend_data.plot(ax=ax)
            st.pyplot(fig)
        else:
            st.error("The dataset must contain a 'year' column.")
    else:
        st.write("Please upload a CSV file in the 'Upload CSV' tab to start analysis.")

# Tab 3: Topic Modeling
with tab3:
    st.write("Topic modeling analysis.")
    if "classified_df" in st.session_state:
        df = st.session_state.classified_df
        if "topic" in df.columns:
            topic_data = (
                df.groupby(["topic", "classification"]).size().unstack(fill_value=0)
            )
            st.write("Frequency of classifications by topic:")
            fig, ax = plt.subplots()
            topic_data.plot(kind="bar", stacked=True, ax=ax)
            st.pyplot(fig)
        else:
            st.error("The dataset must contain a 'topic' column.")
    else:
        st.write("Please upload a CSV file in the 'Upload CSV' tab to start analysis.")

# Tab 4: Upload CSV
with tab4:
    st.write("Upload a CSV file for analysis.")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "text" in df.columns:
            st.write("Classifying and analyzing text data...")
            st.session_state.classified_df = df
            st.write("Data uploaded successfully!")
        else:
            st.error("The CSV file must contain a 'text' column.")
