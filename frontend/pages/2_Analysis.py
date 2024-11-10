import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import os
import numpy as np
import seaborn as sns
from openai import OpenAI
from dotenv import load_dotenv

# Define the data folder
DATA_FOLDER = "pages/data/"

# Custom stopwords
custom_stopwords = {
    "comment",
    "say",
    "singapore",
    "singaporean",
    "people",
    "singaporeans",
    "u",
    "even",
    "will",
    "one",
    "lol",
    "go",
}

st.title("Analysis Overview")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Overview",
        "Frequency Analysis",
        "Intensity Analysis",
        "Findings & Solutions",
        "Upload CSV",
    ]
)

# Tab 1: Overview
with tab1:
    st.markdown(
        """
        ## Welcome to the Text Analysis Dashboard!

        This dashboard provides insights into textual data by analyzing frequency trends,
        intensity changes over time, key findings and solutions.

        **Tabs Overview:**
        - **Frequency Analysis**: View the proportion of each topic across all years.
        - **Intensity Analysis**: Analyze intensity trends and generate word clouds for insights.
        - **Findings & Solutions**: Explore in-depth findings and potential solutions.
        - **Filtered Comments**: View comments filtered by specific topics.
        - **Upload CSV**: Upload your dataset.
        """
    )

# Tab 2: Frequency Analysis
with tab2:
    # Centralize the title
    st.markdown(
        "<h3 style='text-align: center;'>Proportion of Each Topic Across All Years</h3>",
        unsafe_allow_html=True,
    )

    comments_file_path = os.path.join(DATA_FOLDER, "combined_df.csv")
    try:
        df = pd.read_csv(comments_file_path)

        # Ensure required columns exist
        if "Final Topic Name" in df.columns:

            # Filter rows with non-null 'Final Topic Name'
            df_filtered = df[df["Final Topic Name"].notnull()]

            def plot_topic_proportions(df_filtered, topic_column="Final Topic Name"):
                """
                Plots the proportions of each topic in the DataFrame.

                Parameters:
                - df_filtered: The DataFrame containing the data.
                - topic_column: The column name for the topics. Default is "Final Topic Name".
                """
                # Step 1: Count the occurrences of each topic
                topic_counts = (
                    df_filtered.groupby(topic_column).size().reset_index(name="Count")
                )

                # Step 2: Calculate the total count and the percentage for each topic
                total_count = topic_counts["Count"].sum()
                topic_counts["Percentage"] = (topic_counts["Count"] / total_count) * 100

                # Step 3: Plotting the proportions
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(
                    data=topic_counts,
                    x=topic_column,
                    y="Percentage",
                    palette="viridis",
                    ax=ax,
                )

                ax.set_xlabel("Topic")
                ax.set_ylabel("Percentage (%)")
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
                st.pyplot(fig)

            # Call the function to plot proportions
            plot_topic_proportions(df_filtered)

        else:
            st.error("The dataset must contain the 'Final Topic Name' column.")

    except FileNotFoundError:
        st.error(f"{comments_file_path} not found.")
    except Exception as e:
        st.error(f"Error loading or processing the dataset: {e}")

# Tab 3: Intensity Analysis
with tab3:
    subtab1, subtab2, subtab3 = st.tabs(
        ["Net Trend Visualization", "Word Cloud", "Filtered Comments"]
    )

    # Sub-tab 1: Net Trend Visualization
    with subtab1:
        st.write("Net Trend Visualization for Hate and Toxic topics.")

        # Load combined data if available
        combined_file_path = os.path.join(DATA_FOLDER, "combined_df.csv")
        try:
            # Load the combined data
            combined_df = pd.read_csv(combined_file_path)

            # Step 1: Group by topic and count occurrences
            topic_counts = (
                combined_df.groupby("Final Topic Name").size().reset_index(name="Count")
            )
            total_count = topic_counts["Count"].sum()
            topic_counts["Percentage"] = (topic_counts["Count"] / total_count) * 100

            # Step 2: Filter for the top 3 topics
            top_3_topics = topic_counts.nlargest(3, "Count")
            topics_of_interest = top_3_topics["Final Topic Name"].tolist()

            # Step 3: Calculate indices
            def calculate_indices(df, top_topics, years_of_interest):
                topics = top_topics["Final Topic Name"].tolist()
                all_indices_df = pd.DataFrame()

                for topic in topics:
                    indices_data = {"Final Topic Name": topic}
                    for year in years_of_interest:
                        df_topic_year = df[
                            (df["Final Topic Name"] == topic) & (df["year"] == year)
                        ]

                        total_hate_count = df_topic_year[
                            df_topic_year["Classification"].str.startswith("Hate")
                        ].shape[0]
                        total_toxic_count = df_topic_year[
                            df_topic_year["Classification"].str.startswith("Toxic")
                        ].shape[0]

                        if total_hate_count > 0:
                            indices_data.update(
                                {
                                    f"Hate 1 Index {year}": df_topic_year[
                                        df_topic_year["Classification"] == "Hate 1"
                                    ].shape[0]
                                    / total_hate_count,
                                    f"Hate 2 Index {year}": df_topic_year[
                                        df_topic_year["Classification"] == "Hate 2"
                                    ].shape[0]
                                    / total_hate_count,
                                    f"Hate 3 Index {year}": df_topic_year[
                                        df_topic_year["Classification"] == "Hate 3"
                                    ].shape[0]
                                    / total_hate_count,
                                }
                            )

                        if total_toxic_count > 0:
                            indices_data.update(
                                {
                                    f"Toxic 1 Index {year}": df_topic_year[
                                        df_topic_year["Classification"] == "Toxic 1"
                                    ].shape[0]
                                    / total_toxic_count,
                                    f"Toxic 2 Index {year}": df_topic_year[
                                        df_topic_year["Classification"] == "Toxic 2"
                                    ].shape[0]
                                    / total_toxic_count,
                                    f"Toxic 3 Index {year}": df_topic_year[
                                        df_topic_year["Classification"] == "Toxic 3"
                                    ].shape[0]
                                    / total_toxic_count,
                                }
                            )
                    indices_df = pd.DataFrame([indices_data])
                    all_indices_df = pd.concat(
                        [all_indices_df, indices_df], ignore_index=True
                    )

                all_indices_df.fillna(0, inplace=True)
                return all_indices_df

            years_of_interest = [2020, 2021, 2022, 2023]
            all_indices_df = calculate_indices(
                combined_df, top_3_topics, years_of_interest
            )

            # Step 4: Calculate trends using the corrected function
            def calculate_trend_data(all_indices_df, topics_of_interest):
                trend_data = []
                for topic in topics_of_interest:
                    topic_data = all_indices_df[
                        all_indices_df["Final Topic Name"] == topic
                    ]
                    if topic_data.empty:
                        continue

                    trend = {"Final Topic Name": topic}
                    for index_type in ["Hate", "Toxic"]:
                        for level in ["1", "2", "3"]:
                            for start, end in [
                                (2020, 2021),
                                (2021, 2022),
                                (2022, 2023),
                            ]:
                                col_start = f"{index_type} {level} Index {start}"
                                col_end = f"{index_type} {level} Index {end}"
                                val_start = topic_data.get(
                                    col_start, pd.Series([None])
                                ).values[0]
                                val_end = topic_data.get(
                                    col_end, pd.Series([None])
                                ).values[0]
                                trend[
                                    f"{index_type} {level} % Change {start}-{end}"
                                ] = (
                                    ((val_end - val_start) / val_start * 100)
                                    if val_start
                                    else 0
                                )
                    trend_data.append(trend)

                return pd.DataFrame(trend_data)

            trend_df = calculate_trend_data(all_indices_df, topics_of_interest)

            # Step 5: Calculate net trends
            def calculate_net_trends(trend_df):
                years = sorted(
                    set(col.split()[-1] for col in trend_df.columns if "Change" in col)
                )
                hate_columns = [
                    col for col in trend_df.columns if "Hate" in col and "Change" in col
                ]
                toxic_columns = [
                    col
                    for col in trend_df.columns
                    if "Toxic" in col and "Change" in col
                ]
                net_trend_data = []

                for topic in trend_df["Final Topic Name"]:
                    topic_data = trend_df[trend_df["Final Topic Name"] == topic]
                    net_trends = {"Final Topic Name": topic}
                    for year in years:
                        hate_data = [
                            topic_data[col].values[0]
                            for col in hate_columns
                            if year in col
                        ]
                        toxic_data = [
                            topic_data[col].values[0]
                            for col in toxic_columns
                            if year in col
                        ]
                        net_trends[f"Net Hate Trend {year}"] = sum(hate_data)
                        net_trends[f"Net Toxic Trend {year}"] = sum(toxic_data)
                    net_trend_data.append(net_trends)

                return pd.DataFrame(net_trend_data)

            final_trend_df = calculate_net_trends(trend_df)

            # Cache the result for use in Tab 4
            st.session_state["final_trend_df"] = final_trend_df

            # Create hierarchical table with improved aesthetics
            def create_hierarchical_table(df):
                years = sorted(
                    set(col.split()[-1] for col in df.columns if "Net" in col)
                )

                # Define the hierarchical column structure
                columns = [
                    ("", "", "Topic"),  # For the Topic column
                    *[
                        ("", year, label)
                        for year in years
                        for label in ["Hate", "Toxic"]
                    ],
                ]

                data = []
                for _, row in df.iterrows():
                    row_data = [row["Final Topic Name"]]
                    for year in years:
                        row_data.append(row[f"Net Hate Trend {year}"])
                        row_data.append(row[f"Net Toxic Trend {year}"])
                    data.append(row_data)

                multi_columns = pd.MultiIndex.from_tuples(columns)
                styled_df = pd.DataFrame(data, columns=multi_columns)

                return styled_df

            # Custom CSS for a rounded, interactive DataFrame
            custom_css = """
                <style>
                    .dataframe-container {
                        border: 1px solid #ddd;
                        border-radius: 10px;
                        overflow: hidden;
                        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
                    }
                    .dataframe-container table {
                        border-collapse: collapse;
                        width: 100%;
                    }
                    .dataframe-container th, .dataframe-container td {
                        padding: 10px;
                        text-align: center;
                        border-bottom: 1px solid #ddd;
                    }
                    .dataframe-container th {
                        background-color: #f5f5f5;
                        font-weight: bold;
                    }
                    .dataframe-container tr:nth-child(even) {
                        background-color: #f9f9f9;
                    }
                    .dataframe-container tr:hover {
                        background-color: #f1f1f1;
                    }
                </style>
            """

            # Display the updated table
            st.write("Final Net Trends Table:")
            styled_table = create_hierarchical_table(final_trend_df)
            st.markdown(custom_css, unsafe_allow_html=True)  # Apply custom styles
            st.dataframe(styled_table, use_container_width=True)

            # Step 6: Plot net trends
            def plot_net_trends(final_trend_df):
                years = sorted(
                    set(
                        col.split()[-1]
                        for col in final_trend_df.columns
                        if "Net" in col
                    )
                )

                for index, row in final_trend_df.iterrows():
                    topic = row["Final Topic Name"]
                    hate_trends = [row[f"Net Hate Trend {year}"] for year in years]
                    toxic_trends = [row[f"Net Toxic Trend {year}"] for year in years]

                    # Plot Net Hate Trend
                    fig, ax = plt.subplots(figsize=(8, 6))
                    x = np.arange(len(years))
                    width = 0.35

                    ax.bar(
                        x - width / 2,
                        hate_trends,
                        width,
                        label="Net Hate Trend",
                        color="#E57373",
                    )
                    ax.bar(
                        x + width / 2,
                        toxic_trends,
                        width,
                        label="Net Toxic Trend",
                        color="#FFEB3B",
                    )

                    ax.set_title(f"Net Trends for Topic: {topic}")
                    ax.set_xlabel("Year")
                    ax.set_ylabel("Net Trend")
                    ax.set_xticks(x)
                    ax.set_xticklabels(years)
                    ax.legend()

                    st.pyplot(fig)

            plot_net_trends(final_trend_df)

        except FileNotFoundError:
            st.error(f"{combined_file_path} not found.")
        except Exception as e:
            st.error(f"Error: {e}")

    # Sub-tab 2: Word Cloud
    with subtab2:
        st.write("Word Clouds for Topics.")

        # Load necessary data
        comments_file_path = os.path.join(DATA_FOLDER, "combined_df.csv")
        try:
            comments_df = pd.read_csv(comments_file_path)
            final_trend_df = st.session_state["final_trend_df"]

            # Filter positive trends for hate and toxic comments
            def filter_positive_years_separately(final_trend_df):
                positive_trend_data = []
                years = sorted(
                    set(
                        col.split()[-1]
                        for col in final_trend_df.columns
                        if "Net" in col
                    )
                )

                for _, row in final_trend_df.iterrows():
                    topic = row["Final Topic Name"]
                    positive_hate_years = {"Final Topic Name": topic}
                    positive_toxic_years = {"Final Topic Name": topic}

                    for year in years:
                        positive_hate_years[f"Positive Hate Year {year}"] = (
                            row.get(f"Net Hate Trend {year}", 0) > 0
                        )
                        positive_toxic_years[f"Positive Toxic Year {year}"] = (
                            row.get(f"Net Toxic Trend {year}", 0) > 0
                        )

                    positive_trend_data.append(
                        {**positive_hate_years, **positive_toxic_years}
                    )

                return pd.DataFrame(positive_trend_data)

            positive_trend_df = filter_positive_years_separately(final_trend_df)

            # Get comments for positive trend years
            def get_comments_for_positive_years(final_trend_df, comments_df, topic):
                topic_data = final_trend_df[final_trend_df["Final Topic Name"] == topic]
                if topic_data.empty:
                    return pd.DataFrame(), pd.DataFrame()

                years = sorted(
                    set(
                        col.split()[-1]
                        for col in final_trend_df.columns
                        if "Positive" in col
                    )
                )
                hate_comments = []
                toxic_comments = []

                for year in years:
                    if "-" in year:
                        start_year, end_year = map(int, year.split("-"))
                    else:
                        start_year = end_year = int(year)

                    if topic_data[f"Positive Hate Year {year}"].iloc[0]:
                        hate_comments_in_years = comments_df[
                            (comments_df["year"] >= start_year)
                            & (comments_df["year"] <= end_year)
                            & (comments_df["Final Topic Name"] == topic)
                            & (comments_df["Classification"].str.startswith("Hate"))
                        ]
                        hate_comments.append(hate_comments_in_years)

                    if topic_data[f"Positive Toxic Year {year}"].iloc[0]:
                        toxic_comments_in_years = comments_df[
                            (comments_df["year"] >= start_year)
                            & (comments_df["year"] <= end_year)
                            & (comments_df["Final Topic Name"] == topic)
                            & (comments_df["Classification"].str.startswith("Toxic"))
                        ]
                        toxic_comments.append(toxic_comments_in_years)

                return (
                    (
                        pd.concat(hate_comments, ignore_index=True)
                        if hate_comments
                        else pd.DataFrame()
                    ),
                    (
                        pd.concat(toxic_comments, ignore_index=True)
                        if toxic_comments
                        else pd.DataFrame()
                    ),
                )

            # Add ranking to topics based on frequency
            ranked_topics = final_trend_df.assign(Rank=final_trend_df.index + 1)[
                ["Final Topic Name", "Rank"]
            ].sort_values(by="Rank")
            topic_options = ranked_topics.apply(
                lambda row: f"Rank {row['Rank']}: {row['Final Topic Name']}", axis=1
            ).tolist()

            # Select topic to analyze (single dropdown)
            selected_topic = st.selectbox("Select a topic to analyze:", topic_options)

            if selected_topic:
                selected_topic_name = selected_topic.split(": ")[
                    1
                ]  # Extract topic name

                # Retrieve filtered comments based on positive trends
                hate_comments, toxic_comments = get_comments_for_positive_years(
                    positive_trend_df, comments_df, selected_topic_name
                )

                # Generate word clouds
                selected_topic_type = st.radio(
                    "Select type of comments", ["Hate", "Toxic"]
                )
                topic_df = (
                    hate_comments if selected_topic_type == "Hate" else toxic_comments
                )

                def generate_wordcloud(df, topic_name):
                    custom_stopwords = {
                        "comment",
                        "say",
                        "singapore",
                        "singaporean",
                        "people",
                        "singaporeans",
                        "u",
                        "even",
                        "will",
                        "one",
                        "lol",
                        "go",
                    }
                    stopwords = set(STOPWORDS).union(custom_stopwords)
                    topic_text = " ".join(df["Topic_Words"].dropna())
                    topic_text = topic_text.replace(topic_name, "")

                    wordcloud = WordCloud(
                        width=800,
                        height=400,
                        background_color="white",
                        stopwords=stopwords,
                        colormap="coolwarm",
                        random_state=478,
                    ).generate(topic_text)

                    plt.figure(figsize=(10, 5))
                    plt.imshow(wordcloud, interpolation="bilinear")
                    plt.axis("off")
                    plt.title(
                        f"Word Cloud for {topic_name} Comments ({selected_topic_type} Classification)"
                    )
                    st.pyplot(plt)
                    plt.close()

                if not topic_df.empty:
                    st.write(
                        f"Word Cloud for {selected_topic_name} ({selected_topic_type} Comments)"
                    )
                    generate_wordcloud(topic_df, selected_topic_name)
                else:
                    st.warning(
                        f"No {selected_topic_type} comments found for the topic: {selected_topic_name}"
                    )

        except FileNotFoundError:
            st.error(f"{comments_file_path} not found.")
        except Exception as e:
            st.error(f"Error: {e}")

    # Sub-tab 3: Filtered Comments
    with subtab3:
        st.write("Filtered comments.")
        csv_files = {
            "Race Hate Comments": os.path.join(
                DATA_FOLDER, "increase_race_hate_comments.csv"
            ),
            "Race Toxic Comments": os.path.join(
                DATA_FOLDER, "increase_race_toxic_comments.csv"
            ),
            "Crimes Hate Comments": os.path.join(
                DATA_FOLDER, "increase_crimes_hate_comments.csv"
            ),
            "Crimes Toxic Comments": os.path.join(
                DATA_FOLDER, "increase_crimes_toxic_comments.csv"
            ),
            "Gender Hate Comments": os.path.join(
                DATA_FOLDER, "increase_gender_hate_comments.csv"
            ),
            "Gender Toxic Comments": os.path.join(
                DATA_FOLDER, "increase_gender_toxic_comments.csv"
            ),
        }

        selected_topic = st.selectbox(
            "Select a topic to view sequenced comments:", csv_files.keys()
        )
        if selected_topic:
            file_path = csv_files[selected_topic]
            try:
                df = pd.read_csv(file_path)
                st.dataframe(df)
            except FileNotFoundError:
                st.error(f"File not found: {file_path}")
            except Exception as e:
                st.error(f"Error loading file: {e}")

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Tab 4: Findings + Solutions
with tab4:
    st.markdown("### Findings and Solutions")
    st.write(
        "Analyze datasets to identify the main issues causing increased hateful or toxic comments."
    )

    # File paths for datasets
    dataset_files = {
        "Crimes Hate": "pages/data/increase_crimes_hate_comments.csv",
        "Crimes Toxic": "pages/data/increase_crimes_toxic_comments.csv",
        "Gender Hate": "pages/data/increase_gender_hate_comments.csv",
        "Gender Toxic": "pages/data/increase_gender_toxic_comments.csv",
        "Race Hate": "pages/data/increase_race_hate_comments.csv",
        "Race Toxic": "pages/data/increase_race_toxic_comments.csv",
    }

    # Load datasets
    datasets = {}
    for label, file_path in dataset_files.items():
        try:
            datasets[label] = pd.read_csv(file_path)
        except FileNotFoundError:
            st.error(f"File not found: {file_path}")
        except Exception as e:
            st.error(f"Error loading {label} dataset: {e}")

    def analyze_toxicity_once(dfs, model_name="gpt-4o-mini"):
        """
        Analyzes datasets and identifies principal issues contributing to hateful or toxic comments.
        Runs once and caches the result.

        Parameters:
        - dfs: List of tuples (dataset label, DataFrame).
        - model_name: The model to use for OpenAI chat completion.

        Returns:
        - List of tuples (dataset label, analysis result).
        """
        responses = []
        for label, df in dfs:
            df["title_text"] = df["Reddit Title"] + ": " + df["text"]
            prompt_content = " ".join(df["title_text"].tolist())

            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a skilled assistant tasked with analyzing discussions. From the provided text, identify the principal issue that has led to increased hateful or toxic comments. Make it as succinct as possible.",
                        },
                        {"role": "user", "content": prompt_content},
                    ],
                )
                responses.append((label, response.choices[0].message.content))
            except Exception as e:
                responses.append((label, f"Error analyzing {label}: {e}"))
        return responses

    # Run analysis once and cache results in session state
    if "analysis_results" not in st.session_state:
        df_tuples = [(label, df) for label, df in datasets.items()]
        st.session_state["analysis_results"] = analyze_toxicity_once(df_tuples)

    # Display cached results
    for label, result in st.session_state["analysis_results"]:
        st.markdown(f"**Results for {label}:**")
        st.write(result)

# Tab 5: Upload CSV
with tab5:
    st.write("Upload a CSV file for analysis.")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "text" in df.columns:
            st.session_state.classified_df = df
            st.success("Data uploaded successfully!")
        else:
            st.error("The CSV file must contain a 'text' column.")
