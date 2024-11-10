import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import os
import numpy as np
import seaborn as sns
from openai import OpenAI
from dotenv import load_dotenv
import io
from streamlit_lottie import st_lottie
import requests

# Define the data folder
DATA_FOLDER = "pages/data/"

st.set_page_config(layout="wide")

st.title("Analysis Dashboard")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Overview",
        "Frequency Analysis",
        "Intensity Analysis",
        "Findings",
        "Upload CSV",
    ]
)

# Tab 1: Overview
with tab1:
    st.markdown(
        """
        ## Welcome to the Analysis Dashboard!

        This dashboard provides insights into textual data by analyzing frequency trends,
        intensity changes over time, key findings and solutions.

        **Tabs Overview:**
        - **Frequency Analysis**: View the proportion of each topic across all years.
        - **Intensity Analysis**: Analyze intensity trends, generate word clouds for insights and view the comments from the analyzed topics.
        - **Findings**: Explore in-depth findings and potential solutions.
        - **Upload CSV**: Upload your dataset.
        """
    )

# Tab 2: Frequency Analysis
with tab2:
    if (
        "classified_df" in st.session_state
        and not st.session_state["classified_df"].empty
    ):
        # Centralize the title
        st.markdown(
            "<h3 style='text-align: center;'>Proportion of Each Topic Across Selected Years</h3>",
            unsafe_allow_html=True,
        )

        # Create a local copy of the DataFrame for Tab 2
        df_tab2 = st.session_state["classified_df"].copy()

        if "Final Topic Name" in df_tab2.columns and "year" in df_tab2.columns:
            # Filter rows with non-null 'Final Topic Name'
            df_tab2 = df_tab2[df_tab2["Final Topic Name"].notnull()]

            # Create layout: big graph on the left, configurations on the right
            col_graph, col_config = st.columns([5, 1])

            with col_config:
                st.markdown("### Configuration")

                # Year Filter
                years_tab2 = sorted(df_tab2["year"].unique())
                all_years_selected_tab2 = st.checkbox(
                    "All Years", value=True, key="all_years_selected_tab2"
                )

                selected_years_tab2 = st.multiselect(
                    "Select Years",
                    options=years_tab2,
                    default=years_tab2 if all_years_selected_tab2 else [],
                    disabled=all_years_selected_tab2,
                    key="selected_years_tab2",
                )

                # **Removed 'or not selected_years_tab2' condition**
                if all_years_selected_tab2:
                    selected_years_tab2 = years_tab2

                # Topic Filter
                topics_tab2 = sorted(df_tab2["Final Topic Name"].unique())
                all_topics_selected_tab2 = st.checkbox(
                    "All Topics", value=True, key="all_topics_selected_tab2"
                )

                selected_topics_tab2 = st.multiselect(
                    "Select Topics",
                    options=topics_tab2,
                    default=topics_tab2 if all_topics_selected_tab2 else [],
                    disabled=all_topics_selected_tab2,
                    key="selected_topics_tab2",
                )

                # **Removed 'or not selected_topics_tab2' condition**
                if all_topics_selected_tab2:
                    selected_topics_tab2 = topics_tab2

                # Color Palette Selector
                color_palettes = {
                    "Viridis": "viridis",
                    "Plasma": "plasma",
                    "Coolwarm": "coolwarm",
                    "Magma": "magma",
                }
                selected_palette_tab2 = st.selectbox(
                    "Choose a Color Palette",
                    list(color_palettes.keys()),
                    index=0,
                    key="selected_palette_tab2",
                )

            # Filter data based on selections (use local variables)
            df_tab2_filtered = df_tab2[
                (df_tab2["year"].isin(selected_years_tab2))
                & (df_tab2["Final Topic Name"].isin(selected_topics_tab2))
            ]

            with col_graph:

                def plot_topic_proportions(
                    df_filtered, topic_column="Final Topic Name"
                ):
                    """
                    Plots the proportions of each topic in the DataFrame.

                    Parameters:
                    - df_filtered: The DataFrame containing the data.
                    - topic_column: The column name for the topics.
                    """
                    # Initialize the plot
                    fig, ax = plt.subplots(figsize=(12, 8))

                    if df_filtered.empty:
                        # Create an empty plot with grids and axis
                        ax.set_xlim(-0.5, 0.5)  # Placeholder limits
                        ax.set_ylim(0, 100)  # Y-axis range for percentages
                        ax.set_xlabel("Topic")
                        ax.set_ylabel("Percentage (%)")
                        ax.set_xticks([])  # Remove x-ticks for empty plot
                        ax.grid(
                            True, which="both", linestyle="--", linewidth=0.7
                        )  # Add gridlines

                        # Optionally, you can add a placeholder text
                        ax.text(
                            0,
                            50,
                            "No data to display",
                            horizontalalignment="center",
                            verticalalignment="center",
                            fontsize=14,
                            color="gray",
                            alpha=0.6,
                        )
                    else:
                        # Count occurrences of each topic
                        topic_counts = (
                            df_filtered.groupby(topic_column)
                            .size()
                            .reset_index(name="Count")
                        )
                        total_count = topic_counts["Count"].sum()
                        topic_counts["Percentage"] = (
                            topic_counts["Count"] / total_count
                        ) * 100

                        # Plotting
                        sns.barplot(
                            data=topic_counts,
                            x=topic_column,
                            y="Percentage",
                            palette=color_palettes[selected_palette_tab2],
                            ax=ax,
                        )

                        ax.set_xlabel("Topic")
                        ax.set_ylabel("Percentage (%)")
                        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

                        # Add percentage labels on bars
                        for p in ax.patches:
                            ax.annotate(
                                f"{p.get_height():.2f}%",
                                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                                ha="center",
                                va="center",
                                fontsize=10,
                                color="black",
                                xytext=(0, 5),
                                textcoords="offset points",
                            )

                    plt.tight_layout()
                    return fig

                # Generate and display the plot
                fig = plot_topic_proportions(df_tab2_filtered)
                st.pyplot(fig)

                # Enable download of the plot
                buffer = io.BytesIO()
                fig.savefig(buffer, format="png", bbox_inches="tight")
                buffer.seek(0)

                st.download_button(
                    label="Download Graph as PNG",
                    data=buffer,
                    file_name="topic_proportions.png",
                    mime="image/png",
                )

        else:
            st.error(
                "The dataset must contain the 'Final Topic Name' and 'year' columns."
            )
    else:
        st.info("Please upload a CSV file in the 'Upload CSV' tab to proceed.")

# Tab 3: Intensity Analysis
with tab3:
    subtab1, subtab2, subtab3 = st.tabs(
        ["Net Trend Visualization", "Word Cloud", "Filtered Comments"]
    )

    # Sub-tab 1: Net Trend Visualization
    with subtab1:

        # Check if the uploaded CSV is available in session state
        if (
            "classified_df" in st.session_state
            and not st.session_state["classified_df"].empty
        ):
            combined_df = st.session_state["classified_df"]

            try:
                # Step 1: Group by topic and count occurrences
                topic_counts = (
                    combined_df.groupby("Final Topic Name")
                    .size()
                    .reset_index(name="Count")
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

                # Step 4: Calculate trends
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
                        set(
                            col.split()[-1]
                            for col in trend_df.columns
                            if "Change" in col
                        )
                    )
                    hate_columns = [
                        col
                        for col in trend_df.columns
                        if "Hate" in col and "Change" in col
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
                            margin: 0 auto;  /* Center the table */
                            width: 80%;      /* Optional: Control table width */
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

                # Step 6: Plot net trends with consistent y-axis scale and improved spacing
                def plot_net_trends(final_trend_df):
                    years = sorted(
                        set(
                            col.split()[-1]
                            for col in final_trend_df.columns
                            if "Net" in col
                        )
                    )

                    # Calculate global min and max for y-axis
                    all_hate_trends = final_trend_df[
                        [f"Net Hate Trend {year}" for year in years]
                    ].values.flatten()
                    all_toxic_trends = final_trend_df[
                        [f"Net Toxic Trend {year}" for year in years]
                    ].values.flatten()

                    global_min = min(all_hate_trends.min(), all_toxic_trends.min())
                    global_max = max(all_hate_trends.max(), all_toxic_trends.max())

                    # Add padding to the y-axis
                    y_padding = (global_max - global_min) * 0.1
                    global_min -= y_padding
                    global_max += y_padding

                    for index, row in final_trend_df.iterrows():
                        topic = row["Final Topic Name"]
                        hate_trends = [row[f"Net Hate Trend {year}"] for year in years]
                        toxic_trends = [
                            row[f"Net Toxic Trend {year}"] for year in years
                        ]

                        # Plot Net Hate and Toxic Trends
                        fig, ax = plt.subplots(
                            figsize=(6, 4)  # Reduced width and height for smaller plot
                        )
                        x = np.arange(len(years))
                        width = (
                            0.3  # Reduced bar width for better spacing in smaller plots
                        )

                        bars_hate = ax.bar(
                            x - width / 2,
                            hate_trends,
                            width,
                            label="Net Hate Trend",
                            color="#D32F2F",
                            alpha=0.8,
                        )
                        bars_toxic = ax.bar(
                            x + width / 2,
                            toxic_trends,
                            width,
                            label="Net Toxic Trend",
                            color="#FFEB3B",
                            alpha=0.8,
                        )

                        ax.set_title(
                            f"Net Trends for Topic: {topic}", fontsize=8, weight="bold"
                        )
                        ax.set_xlabel("Year", fontsize=6)
                        ax.set_ylabel("Net Trend", fontsize=6)
                        ax.set_xticks(x)
                        ax.set_xticklabels(years, rotation=45, ha="right", fontsize=6)

                        # Set y-axis tick font size
                        ax.tick_params(axis="y", labelsize=6)

                        # Set consistent y-axis limits with padding
                        ax.set_ylim(global_min, global_max)

                        # Add numbers on bars
                        for bar in bars_hate:
                            ax.annotate(
                                f"{bar.get_height():.2f}",  # Display height as a number
                                xy=(
                                    bar.get_x() + bar.get_width() / 2,
                                    bar.get_height(),
                                ),
                                xytext=(
                                    0,
                                    3,
                                ),  # Offset the text position slightly above the bar
                                textcoords="offset points",
                                ha="center",
                                va="center",
                                fontsize=6,
                                color="black",
                            )

                        for bar in bars_toxic:
                            ax.annotate(
                                f"{bar.get_height():.2f}",
                                xy=(
                                    bar.get_x() + bar.get_width() / 2,
                                    bar.get_height(),
                                ),
                                xytext=(0, 3),
                                textcoords="offset points",
                                ha="center",
                                va="center",
                                fontsize=6,
                                color="black",
                            )

                        # Add gridlines
                        ax.grid(
                            True, which="both", linestyle="--", linewidth=0.5, alpha=0.7
                        )

                        # Tighten layout
                        plt.tight_layout()

                        # Show the plot in Streamlit
                        st.pyplot(fig)

                        # Save the plot to a BytesIO buffer
                        buffer = io.BytesIO()
                        fig.savefig(buffer, format="png", bbox_inches="tight")
                        buffer.seek(0)

                        # Provide a download button
                        st.download_button(
                            label="Download Graph as PNG",
                            data=buffer,
                            file_name=f"net_trends_{topic.replace(' ', '_')}.png",
                            mime="image/png",
                        )

                        plt.close(fig)  # Close the plot to free memory

                plot_net_trends(final_trend_df)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.info("Please upload a CSV file in the 'Upload CSV' tab to proceed.")

    # Sub-tab 2: Word Cloud
    with subtab2:

        # Ensure uploaded data and session state are available
        if (
            "classified_df" not in st.session_state
            or st.session_state["classified_df"].empty
        ):
            st.info("Please upload a CSV file in the 'Upload CSV' tab to proceed.")
        else:
            comments_df = st.session_state["classified_df"]
            final_trend_df = st.session_state.get("final_trend_df", pd.DataFrame())

            if final_trend_df.empty:
                st.error("Final trend data is not available.")
            else:
                # Use ranked topics from Sub-tab 1
                if "final_trend_df" in st.session_state:
                    top_3_topics = (
                        st.session_state["final_trend_df"]["Final Topic Name"]
                        .iloc[:3]
                        .tolist()
                    )  # Get top 3 ranked topics
                else:
                    top_3_topics = []

                # Generate positive trends for these topics
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

                def get_comments_for_positive_years(
                    final_trend_df, comments_df, topics_of_interest
                ):
                    filtered_hate_comments_dict = {}
                    filtered_toxic_comments_dict = {}

                    years = sorted(
                        set(
                            col.split()[-1]
                            for col in final_trend_df.columns
                            if "Positive" in col
                        )
                    )

                    for topic in topics_of_interest:
                        topic_data = final_trend_df[
                            final_trend_df["Final Topic Name"] == topic
                        ]

                        hate_comments = []
                        toxic_comments = []

                        if not topic_data.empty:
                            for year in years:
                                start_year, end_year = map(int, year.split("-"))

                                positive_hate_column = f"Positive Hate Year {year}"
                                if (
                                    positive_hate_column in topic_data.columns
                                    and topic_data[positive_hate_column].iloc[0]
                                ):
                                    hate_comments_in_years = comments_df[
                                        (comments_df["year"] > start_year)
                                        & (comments_df["year"] <= end_year)
                                        & (comments_df["Final Topic Name"] == topic)
                                        & (
                                            comments_df[
                                                "Classification"
                                            ].str.startswith("Hate")
                                        )
                                    ]
                                    hate_comments.append(hate_comments_in_years)

                                positive_toxic_column = f"Positive Toxic Year {year}"
                                if (
                                    positive_toxic_column in topic_data.columns
                                    and topic_data[positive_toxic_column].iloc[0]
                                ):
                                    toxic_comments_in_years = comments_df[
                                        (comments_df["year"] > start_year)
                                        & (comments_df["year"] <= end_year)
                                        & (comments_df["Final Topic Name"] == topic)
                                        & (
                                            comments_df[
                                                "Classification"
                                            ].str.startswith("Toxic")
                                        )
                                    ]
                                    toxic_comments.append(toxic_comments_in_years)

                            if hate_comments:
                                filtered_hate_comments_dict[topic] = pd.concat(
                                    hate_comments, ignore_index=True
                                )
                            if toxic_comments:
                                filtered_toxic_comments_dict[topic] = pd.concat(
                                    toxic_comments, ignore_index=True
                                )

                    return filtered_hate_comments_dict, filtered_toxic_comments_dict

                filtered_hate_comments_dict, filtered_toxic_comments_dict = (
                    get_comments_for_positive_years(
                        positive_trend_df, comments_df, top_3_topics
                    )
                )

                def generate_wordcloud(df, topic_name, custom_stopwords):
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
                    plt.title(f"Word Cloud for {topic_name}")
                    st.pyplot(plt)
                    plt.close()

                custom_stopwords = {
                    "comment",
                    "say",
                    "singapore",
                    "people",
                    "u",
                    "will",
                    "one",
                    "lol",
                }

                # Word Cloud generation and calculation process
                for topic in top_3_topics:
                    st.subheader(f"Analysis for {topic}")
                    hate_df = filtered_hate_comments_dict.get(topic, pd.DataFrame())
                    toxic_df = filtered_toxic_comments_dict.get(topic, pd.DataFrame())

                    if not hate_df.empty:
                        st.write(f"Word Cloud for {topic} (Hate)")
                        generate_wordcloud(hate_df, topic, custom_stopwords)

                    if not toxic_df.empty:
                        st.write(f"Word Cloud for {topic} (Toxic)")
                        generate_wordcloud(toxic_df, topic, custom_stopwords)

                    def filter_and_sequence_comments(df, n=20):
                        """
                        Filters the DataFrame based on the most frequently occurring exact 'Topic_Words' list,
                        extracts the title from the URL, and sequences comments by intensity level within that subset.
                        """
                        if "Topic_Words" not in df.columns or "link" not in df.columns:
                            return (
                                pd.DataFrame()
                            )  # Return empty DataFrame if required columns are missing

                        # Step 1: Count occurrences of each unique list in 'Topic_Words'
                        topic_words_counts = (
                            df["Topic_Words"].apply(tuple).value_counts()
                        )

                        # Step 2: Identify the most frequent 'Topic_Words' list
                        if not topic_words_counts.empty:
                            top_topic_words = topic_words_counts.idxmax()
                        else:
                            return pd.DataFrame()

                        # Step 3: Filter DataFrame for rows matching the most frequent 'Topic_Words'
                        filtered_df = df[
                            df["Topic_Words"].apply(tuple) == top_topic_words
                        ].copy()

                        # Step 4: Extract intensity levels
                        filtered_df["Intensity"] = (
                            filtered_df["Classification"]
                            .str.extract(r"(\d)")
                            .astype(float)
                        )
                        intensity_order = [3, 2, 1]
                        filtered_df["Intensity"] = pd.Categorical(
                            filtered_df["Intensity"],
                            categories=intensity_order,
                            ordered=True,
                        )
                        filtered_df = filtered_df.sort_values(by="Intensity")

                        # Step 5: Extract 'Reddit Title' if 'link' column exists and is not empty
                        if "link" in filtered_df.columns:
                            filtered_df["Reddit Title"] = (
                                filtered_df["link"]
                                .astype(str)  # Ensure all entries are strings
                                .str.extract(r"/comments/\w+/([^/]+)/")
                                .fillna("")  # Handle NaN values
                            )
                            filtered_df["Reddit Title"] = filtered_df[
                                "Reddit Title"
                            ].str.replace("_", " ")

                        # Drop the temporary 'Intensity' column
                        return filtered_df.drop(columns=["Intensity"]).head(n)

                    st.session_state[f"increase_{topic.lower()}_hate_comments"] = (
                        filter_and_sequence_comments(hate_df)
                    )
                    st.session_state[f"increase_{topic.lower()}_toxic_comments"] = (
                        filter_and_sequence_comments(toxic_df)
                    )

    # Sub-tab 3: Filtered Comments
    with subtab3:
        # Ensure the uploaded CSV is available
        if (
            "classified_df" not in st.session_state
            or st.session_state["classified_df"].empty
        ):
            st.info("Please upload a CSV file in the 'Upload CSV' tab to proceed.")
        else:
            final_trend_df = st.session_state.get("final_trend_df", pd.DataFrame())

            if final_trend_df.empty:
                st.error("Final trend data is not available.")
            else:
                # Extract ranked topics and normalize to title case
                ranked_topics = [
                    topic.title()
                    for topic in final_trend_df["Final Topic Name"].tolist()
                ]

                # Dynamically fetch session state keys for filtered comments
                session_data_keys = {
                    f"{topic.title()} {comment_type.title()} Comments": session_key
                    for session_key in st.session_state.keys()
                    if session_key.startswith("increase_")
                    and session_key.endswith("_comments")
                    for topic, comment_type in [
                        session_key.replace("increase_", "")
                        .replace("_comments", "")
                        .split("_", 1)
                    ]
                }

                if not session_data_keys:
                    st.warning("No filtered comments available in session state.")
                else:
                    # Maintain order: Ranked topics first, Hate before Toxic within each topic
                    sorted_keys = [
                        f"{topic} {comment_type} Comments"
                        for topic in ranked_topics
                        for comment_type in ["Hate", "Toxic"]
                        if f"{topic} {comment_type} Comments" in session_data_keys
                    ]

                    # Populate selectbox options
                    selected_topic = st.selectbox(
                        "Select a topic to view sequenced comments:", sorted_keys
                    )

                    if selected_topic:
                        session_key = session_data_keys[selected_topic]

                        try:
                            # Access the corresponding DataFrame in session state
                            if session_key in st.session_state:
                                df = st.session_state[session_key]
                                if not df.empty:
                                    # Select only the desired columns
                                    columns_to_display = [
                                        "text",
                                        "timestamp",
                                        "username",
                                        "link",
                                        "Sensitive Group",
                                        "Classification",
                                        "Topic_Words",
                                        "Final Topic Name",
                                        "Reddit Title",
                                    ]
                                    # Filter DataFrame to show only the specified columns
                                    filtered_df = df[columns_to_display]
                                    st.dataframe(filtered_df)
                                else:
                                    st.warning(
                                        f"No data available for {selected_topic}."
                                    )
                            else:
                                st.error(
                                    f"Data for {selected_topic} is not available in session state."
                                )
                        except Exception as e:
                            st.error(f"Error loading data: {e}")

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Function to load Lottie animations
def load_lottie_url(url: str):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            st.warning("⚠️ Failed to load animation. Using default fallback.")
            return None
        return response.json()
    except Exception as e:
        st.error(f"Error loading Lottie animation: {e}")
        return None


# Replace this with a valid Lottie animation URL
lottie_analysis_url = (
    "https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json"  # Example URL
)
lottie_analysis = load_lottie_url(lottie_analysis_url)

# Tab 4: Findings
with tab4:
    if (
        "classified_df" not in st.session_state
        or st.session_state["classified_df"].empty
    ):
        st.info("Please upload a CSV file in the 'Upload CSV' tab to proceed.")
    else:
        st.markdown(
            "<h3 style='text-align: left; color: #2E86C1;'>🔍 Findings</h3>",
            unsafe_allow_html=True,
        )

        # Extract analyzed topics dynamically
        final_trend_df = st.session_state.get("final_trend_df", pd.DataFrame())
        topics_analyzed = (
            final_trend_df["Final Topic Name"].tolist()
            if not final_trend_df.empty
            else []
        )

        col1, col2 = st.columns([1, 3])
        with col1:
            if lottie_analysis:
                st_lottie(lottie_analysis, height=150, key="analysis_animation")
            else:
                st.markdown("⚙️ *(Animation unavailable, proceeding...)*")
        with col2:
            topics_html = ", ".join(
                [f"<strong>{topic}</strong>" for topic in topics_analyzed[:5]]
            )  # Show first 5 topics
            st.markdown(
                f"""
                <div style='display: flex; align-items: flex-start; height: 100%; margin-top: 40px;'>
                    <p style='font-size: 16px; color: #BFC9CA;'>
                    The following topics have been analyzed and identified as problematic: {topics_html}.
                    These insights highlight areas of increased hateful or toxic behavior.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if final_trend_df.empty:
            st.error("Final trend data is not available.")
        else:
            # Extract and organize datasets
            ranked_topics = [
                topic.lower() for topic in final_trend_df["Final Topic Name"].tolist()
            ]
            session_data_keys = {
                f"{topic.lower()} {comment_type}": session_key
                for session_key in st.session_state.keys()
                if session_key.startswith("increase_")
                and session_key.endswith("_comments")
                for topic, comment_type in [
                    session_key.replace("increase_", "")
                    .replace("_comments", "")
                    .split("_", 1)
                ]
                if topic.lower() in ranked_topics
            }

            if not session_data_keys:
                st.warning("No datasets available for analysis.")
            else:
                sorted_keys = [
                    (
                        f"{topic.title()} {comment_type.title()}",
                        session_data_keys[f"{topic.lower()} {comment_type}"],
                    )
                    for topic in ranked_topics
                    for comment_type in ["hate", "toxic"]
                    if f"{topic.lower()} {comment_type}" in session_data_keys
                ]

                datasets = {
                    label: st.session_state[session_key]
                    for label, session_key in sorted_keys
                    if session_key in st.session_state
                }

                if not datasets:
                    st.warning("No datasets available for analysis.")
                else:
                    # Filter and Insights in the Same Row
                    filter_col, insights_col = st.columns([1, 3])

                    with filter_col:
                        # Align Filters heading with Key Insights and update emoji
                        st.markdown(
                            "<h4 style='color: #117A65;'>🛠️ Filters</h4>",
                            unsafe_allow_html=True,
                        )

                        # Dropdown for filtering by type
                        filter_by_type = st.selectbox(
                            "Filter by Comment Type",
                            options=["All", "Hate", "Toxic"],
                            help="Choose whether to view findings for Hate or Toxic comments only.",
                        )

                        # Search box for filtering by keyword
                        search_term = st.text_input(
                            "Search within findings",
                            help="Enter keywords to search within the findings.",
                        )

                    with insights_col:
                        st.markdown(
                            "<h4 style='color: #117A65;'>💡 Key Insights</h4>",
                            unsafe_allow_html=True,
                        )

                        # Analyze data if not already cached
                        if "analysis_results" not in st.session_state:
                            with st.spinner("Analyzing data..."):

                                def analyze_toxicity_once(dfs, model_name="gpt-4"):
                                    responses = []
                                    for identifier, df in dfs:
                                        if df.empty:
                                            responses.append(
                                                (
                                                    identifier,
                                                    "No data available for analysis.",
                                                )
                                            )
                                            continue
                                        df["title_text"] = (
                                            df["Reddit Title"] + ": " + df["text"]
                                        )
                                        prompt_content = " ".join(
                                            df["title_text"].tolist()
                                        )
                                        prompt_content = prompt_content[
                                            :2048
                                        ]  # Limit token size
                                        issue_type = (
                                            "increased hateful comments"
                                            if "Hate" in identifier
                                            else "increased toxic comments"
                                        )
                                        try:
                                            response = client.chat.completions.create(
                                                model=model_name,
                                                messages=[
                                                    {
                                                        "role": "system",
                                                        "content": (
                                                            "You are a skilled assistant tasked with analyzing discussions. "
                                                            f"From the provided text, identify the principal issue that has led to {issue_type}. "
                                                            "Make it as succinct as possible."
                                                        ),
                                                    },
                                                    {
                                                        "role": "user",
                                                        "content": prompt_content,
                                                    },
                                                ],
                                            )
                                            responses.append(
                                                (
                                                    identifier,
                                                    response.choices[0].message.content,
                                                )
                                            )
                                        except Exception as e:
                                            responses.append(
                                                (
                                                    identifier,
                                                    f"Error analyzing {identifier}: {e}",
                                                )
                                            )
                                    return responses

                                df_tuples = [
                                    (label, df) for label, df in datasets.items()
                                ]
                                st.session_state["analysis_results"] = (
                                    analyze_toxicity_once(df_tuples)
                                )

                        # Display filtered results
                        filtered_results = [
                            (label, result)
                            for label, result in st.session_state["analysis_results"]
                            if (
                                filter_by_type == "All"
                                or filter_by_type.lower() in label.lower()
                            )
                            and (
                                search_term.lower() in result.lower()
                                or search_term.lower() in label.lower()
                            )
                        ]

                        if filtered_results:
                            for label, result in filtered_results:
                                with st.expander(f"📋 {label}", expanded=False):
                                    st.markdown(
                                        f"""
                                        <div style='border: 1px solid #D5DBDB; border-radius: 8px; padding: 10px; background-color: #FDFEFE;'>
                                            <p style='color: #515A5A; font-size: 14px;'>{result}</p>
                                        </div>
                                        """,
                                        unsafe_allow_html=True,
                                    )
                        else:
                            st.warning("No matching findings based on your filters.")

# Tab 5: Upload CSV
with tab5:
    st.write("Upload a CSV file for analysis.")

    # Initialize a flag to control rerun
    if "file_uploaded" not in st.session_state:
        st.session_state["file_uploaded"] = False

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file and not st.session_state["file_uploaded"]:
        try:
            df = pd.read_csv(uploaded_file)
            if "text" in df.columns:
                st.session_state["classified_df"] = df  # Save to session state
                st.session_state["file_uploaded"] = True  # Set the flag to avoid reruns
                st.success("Data uploaded and saved successfully!")
                st.write("Preview of the uploaded data:")
                st.dataframe(df.head())  # Display a preview of the uploaded data

                # Rerun the app to update state across tabs
                st.rerun()
            else:
                st.error("The CSV file must contain a 'text' column.")
        except Exception as e:
            st.error(f"An error occurred while loading the CSV file: {e}")
