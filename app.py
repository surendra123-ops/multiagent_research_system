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
    page_title="ResearchMind",
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

/* Main Layout */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Hero Section */
.hero {
    padding: 2rem 0 1rem 0;
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

/* Sidebar Cards */
.status-card {
    background: #121826;
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid #202939;
    margin-bottom: 1rem;
    color: white;
}

/* Metric Cards */
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
    padding: 0.9rem;
    font-size: 1rem;
}

/* Input */
.stTextInput input {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #2a3441 !important;
}

/* Report Box */
.report-box {
    background: #111827;
    padding: 2rem;
    border-radius: 18px;
    border: 1px solid #1f2937;
    color: white;
}

/* Footer */
.footer {
    text-align: center;
    color: #7c8593;
    padding-top: 3rem;
    font-size: 0.9rem;
}

.agent-heading {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

.agent-desc {
    color: #9aa4b2;
    font-size: 0.85rem;
}

.agent-status {
    margin-top: 0.8rem;
    font-weight: 600;
}

/* Progress */
.stProgress > div > div > div {
    background-color: #ff7b1a;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

default_states = {
    "report": "",
    "critic": "",
    "search": "",
    "reader": "",
    "search_status": "🟢 Ready",
    "reader_status": "🟢 Ready",
    "writer_status": "🟢 Ready",
    "critic_status": "🟢 Ready"
}

for key, value in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("🧠 ResearchMind")

    st.markdown("---")

    st.markdown("## 🤖 AI Agent Status")

    st.markdown(f"""
    <div class="status-card">
        <div class="agent-heading">🔍 Search Agent</div>
        <div class="agent-desc">
            Searches the web for relevant and updated information.
        </div>
        <div class="agent-status">
            Status: {st.session_state.search_status}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="status-card">
        <div class="agent-heading">📄 Reader Agent</div>
        <div class="agent-desc">
            Extracts and analyzes detailed content from sources.
        </div>
        <div class="agent-status">
            Status: {st.session_state.reader_status}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="status-card">
        <div class="agent-heading">✍️ Writer Agent</div>
        <div class="agent-desc">
            Generates a structured professional report.
        </div>
        <div class="agent-status">
            Status: {st.session_state.writer_status}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="status-card">
        <div class="agent-heading">🧐 Critic Agent</div>
        <div class="agent-desc">
            Reviews and evaluates the final report quality.
        </div>
        <div class="agent-status">
            Status: {st.session_state.critic_status}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">
        Research<span class="hero-gradient">Mind</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

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
        <h2>Live</h2>
        <p>Research Pipeline</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric">
        <h2>Smart</h2>
        <p>AI Reports</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------
# INPUT
# ---------------------------------------------------

topic = st.text_input(
    "Research Topic",
    placeholder="Example: Future of AI Agents in 2026"
)

run = st.button("🚀 Generate Research Report")

# ---------------------------------------------------
# RUN PIPELINE
# ---------------------------------------------------

if run:

    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    # Reset states
    st.session_state.search_status = "🟡 Running"
    st.session_state.reader_status = "⚪ Waiting"
    st.session_state.writer_status = "⚪ Waiting"
    st.session_state.critic_status = "⚪ Waiting"

    progress = st.progress(0)

    status = st.empty()

    try:

        # ---------------------------------------------------
        # SEARCH AGENT
        # ---------------------------------------------------

        status.info("🔍 Search Agent is gathering information...")

        search_agent = build_search_agent()

        sr = search_agent.invoke({
            "messages": [
                ("user", f"Find detailed information about {topic}")
            ]
        })

        search_output = str(sr["messages"][-1].content)

        st.session_state.search = search_output

        st.session_state.search_status = "✅ Completed"
        st.session_state.reader_status = "🟡 Running"

        progress.progress(25)

        # ---------------------------------------------------
        # READER AGENT
        # ---------------------------------------------------

        status.info("📄 Reader Agent is extracting deep insights...")

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

        st.session_state.reader_status = "✅ Completed"
        st.session_state.writer_status = "🟡 Running"

        progress.progress(50)

        # ---------------------------------------------------
        # WRITER AGENT
        # ---------------------------------------------------

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

        st.session_state.writer_status = "✅ Completed"
        st.session_state.critic_status = "🟡 Running"

        progress.progress(75)

        # ---------------------------------------------------
        # CRITIC AGENT
        # ---------------------------------------------------

        status.info("🧐 Critic Agent is reviewing report quality...")

        critic = critic_chain.invoke({
            "report": report
        })

        st.session_state.critic = critic

        st.session_state.critic_status = "✅ Completed"

        progress.progress(100)

        status.success("✅ Research Pipeline Completed Successfully")

    except Exception as e:

        st.error(f"Error: {str(e)}")

        st.session_state.search_status = "❌ Failed"
        st.session_state.reader_status = "❌ Failed"
        st.session_state.writer_status = "❌ Failed"
        st.session_state.critic_status = "❌ Failed"

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

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("🔍 Search Agent Output"):
        st.write(st.session_state.search)

    with st.expander("📄 Reader Agent Output"):
        st.write(st.session_state.reader)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown(f"""
<div class="footer">
Built for Intelligent Multi-Agent Research Workflows
<br><br>
© {datetime.now().year} ResearchMind
</div>
""", unsafe_allow_html=True)
