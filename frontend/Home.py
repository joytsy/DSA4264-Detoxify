import streamlit as st

# Set the page configuration
st.set_page_config(layout="centered", page_title="LionGuard Pro Max")

# Custom CSS for interactive, tech-style app title with a gradient scrolling effect
st.markdown(
    """
    <style>
    .title {
        font-size: 50px;
        font-weight: 700;
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        letter-spacing: 2px;
        margin-bottom: 20px;
        background: linear-gradient(90deg, #FF0000, #FF8C00, #FFD700, #FF8C00, #FF0000);
        background-size: 400% auto;
        color: #FFF;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientScroll 5s ease infinite;
    }
    @keyframes gradientScroll {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }
    .subtitle {
        font-size: 24px;
        font-weight: 500;
        text-align: center;
        margin-top: -10px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #666;
    }
    .content {
        text-align: center;
        font-size: 18px;
        line-height: 1.6;
        margin-top: 20px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .sidebar-message {
        font-size: 16px;
        font-weight: 600;
        text-align: center;
        margin-top: 20px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #FFA500; /* Amber color */
        background: linear-gradient(90deg, #FF8C00, #FFD700, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientScroll 5s ease infinite;
    }
    .footer {
        text-align: center;
        font-size: 18px;
        font-weight: 500;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        margin-top: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Interactive, tech-style app title with a gradient scrolling effect
st.markdown("<div class='title'>LionGuard Pro Max</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>The Ultimate Solution for Managing Toxic and Hateful Comments</div>",
    unsafe_allow_html=True,
)

# Custom glowing amber sidebar message
st.sidebar.markdown(
    "<div class='sidebar-message'>Select a page above to get started!</div>",
    unsafe_allow_html=True,
)

# Launch-like product introduction
st.markdown(
    """
    <div class='content'>
        Experience the power of <strong>LionGuard Pro Max</strong> — the ultimate app for classifying
        and analyzing toxic and hateful comments. Effortlessly upload your data, automate insights, and
        take control of your online environment with ease.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    ---

    ### Key Features:
    - **Effortless Classification**: Navigate to the **Analysis** page, upload your CSV, and let our AI model
      do the heavy lifting by classifying thousands of comments in seconds.
    - **Automated Insights**: Our app delivers in-depth analysis and highlights critical areas, so you know
      exactly where to focus.
    - **Comprehensive Solutions**: From detection to resolution, LionGuard Pro Max ensures that you have the
      insights needed to tackle toxicity head-on.
    """,
    unsafe_allow_html=True,
)

# Centralized footer text
st.markdown(
    "<div class='footer'>Experience the future of comment moderation and analysis today. 🚀</div>",
    unsafe_allow_html=True,
)
