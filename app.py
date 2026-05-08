import streamlit as st
import time
from datetime import datetime
from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b0f19;
    color: white;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Hero */
.hero {
    padding: 2rem 0;
}

.hero-title {
    font-size: 4rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.5rem;
}

.hero-gradient {
    background: linear-gradient(90deg, #ff6b00, #ffb347);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    color: #9aa4b2;
    font-size: 1.1rem;
}

/* Cards */
.card {
    background: #111827;
    padding: 1.2rem;
    border-radius: 18px;
    border: 1px solid #1f2937;
    margin-bottom: 1rem;
}

/* Status cards */
.status-card {
    background: #121826;
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid #202939;
}

/* Metric */
.metric {
    background: #111827;
    padding: 1rem;
    border-radius: 14px;
    text-align: center;
    border: 1px solid #1f2937;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    background: linear-gradient(90deg,#ff6b00,#ff9248);
    color: white;
    border: none;
    font-weight: 700;
    padding: 0.8rem;
    font-size: 1rem;
}

/* Input */
.stTextInput input {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #2a3441 !important;
}

/* Report */
.report-box {
    background: #111827;
    padding: 2rem;
    border-radius: 18px;
    border: 1px solid #1f2937;
}

/* Footer */
.footer {
    text-align: center;
    color: #7c8593;
    padding-top: 3rem;
    font-size: 0.9rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "report" not in st.session_state:
    st.session_state.report = ""

if "critic" not in st.session_state:
    st.session_state.critic = ""

if "search" not in st.session_state:
    st.session_state.search = ""

if "reader" not in st.session_state:
    st.session_state.reader = ""

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("🧠 ResearchMind")

    st.markdown("---")

    st.markdown("### System Status")

    st.success("Groq API Connected")

    st.markdown("---")

    st.markdown("### AI Agents")

    st.markdown("""
    ✅ Search Agent  
    ✅ Reader Agent  
    ✅ Writer Agent  
    ✅ Critic Agent
    """)

    st.markdown("---")

    st.markdown("### Features")

    st.markdown("""
    - Web Search
    - URL Scraping
    - AI Report Generation
    - AI Critic Review
    - Markdown Export
    """)

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">
        Research<span class="hero-gradient">Mind</span>
    </div>

    <div class="hero-sub">
        Multi-Agent AI Research System powered by LangChain + Groq
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TOP METRICS
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric">
        <h2>4</h2>
        <p>AI Agents</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric">
        <h2>Groq</h2>
        <p>LLM Engine</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric">
        <h2>Live</h2>
        <p>Web Search</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric">
        <h2>AI</h2>
        <p>Research Reports</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------
# INPUT
# ---------------------------------------------------

topic = st.text_input(
    "Research Topic",
    placeholder="Enter a topic like: Future of AI Agents in 2026"
)

run = st.button("🚀 Generate Research Report")

# ---------------------------------------------------
# PIPELINE
# ---------------------------------------------------

if run:

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    progress = st.progress(0)

    status = st.empty()

    try:

        # -----------------------------------------
        # SEARCH AGENT
        # -----------------------------------------

        status.info("🔍 Search Agent is gathering information...")

        search_agent = build_search_agent()

        sr = search_agent.invoke({
            "messages": [
                ("user", f"Find detailed information about {topic}")
            ]
        })

        search_output = str(sr["messages"][-1].content)

        st.session_state.search = search_output

        progress.progress(25)

        # -----------------------------------------
        # READER AGENT
        # -----------------------------------------

        status.info("📄 Reader Agent is scraping content...")

        reader_agent = build_reader_agent()

        rr = reader_agent.invoke({
            "messages": [
                ("user",
                 f"Based on this research:\n\n{search_output}\n\n"
                 f"Find the best URL and extract detailed insights.")
            ]
        })

        reader_output = str(rr["messages"][-1].content)

        st.session_state.reader = reader_output

        progress.progress(50)

        # -----------------------------------------
        # WRITER
        # -----------------------------------------

        status.info("✍️ Writer Agent is generating report...")

        combined_research = f"""
        SEARCH RESULTS:
        {search_output}

        SCRAPED CONTENT:
        {reader_output}
        """

        report = writer_chain.invoke({
            "topic": topic,
            "research": combined_research
        })

        st.session_state.report = report

        progress.progress(75)

        # -----------------------------------------
        # CRITIC
        # -----------------------------------------

        status.info("🧐 Critic Agent is reviewing report...")

        critic = critic_chain.invoke({
            "report": report
        })

        st.session_state.critic = critic

        progress.progress(100)

        status.success("✅ Research Pipeline Completed")

    except Exception as e:
        st.error(f"Error: {str(e)}")

# ---------------------------------------------------
# RESULTS
# ---------------------------------------------------

if st.session_state.report:

    st.markdown("## 📝 Final Research Report")

    st.markdown(
        f"""
        <div class="report-box">
        {st.session_state.report}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.download_button(
        label="⬇ Download Report",
        data=st.session_state.report,
        file_name=f"research_report_{int(time.time())}.md",
        mime="text/markdown"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("## 🧐 Critic Feedback")

    st.code(st.session_state.critic)

    with st.expander("🔍 Search Agent Output"):
        st.write(st.session_state.search)

    with st.expander("📄 Reader Agent Output"):
        st.write(st.session_state.reader)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown(f"""
<div class="footer">
Built with LangChain • Groq • Streamlit • Multi-Agent AI System
<br><br>
{datetime.now().year} © ResearchMind
</div>
""", unsafe_allow_html=True)
