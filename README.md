# 🧠 ResearchMind

Deploy Link: https://multiagentresearchsystemgit-kndp9slvewlj5f4njdrwvr.streamlit.app/

ResearchMind is a Multi-Agent AI Research System built using Python, LangChain, Groq, Tavily Search API, and Streamlit.

This project can:
- Search the web for information
- Scrape detailed content from websites
- Generate research reports using AI
- Review and evaluate the generated report

It uses multiple AI agents working together in a research pipeline.

---

# 🚀 Features

- Multi-Agent AI Workflow
- Web Search Integration
- Website Content Scraping
- AI Research Report Generation
- AI Critic Feedback
- Modern Streamlit UI
- Live Agent Status Updates
- Download Research Reports

---

# 🏗️ Agents Used

| Agent | Work |
|---|---|
| 🔍 Search Agent | Searches web for information |
| 📄 Reader Agent | Scrapes detailed content |
| ✍️ Writer Agent | Generates research report |
| 🧐 Critic Agent | Reviews report quality |

---

# ⚙️ Tech Stack

- Python
- LangChain
- Groq API
- Tavily API
- Streamlit
- BeautifulSoup
- Requests

---

# 📂 Project Structure

```bash
project/
│
├── app.py
├── agents.py
├── tools.py
├── requirements.txt
├── .env
└── README.md
```

---

# 🔧 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/researchmind.git

cd researchmind
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create `.env` file:

```env
GROQ_API_KEY=your_groq_api_key

TAVILY_API_KEY=your_tavily_api_key
```

---

# ▶️ Run Project

```bash
streamlit run app.py
```

---

# 🌐 Deployment

This project can be deployed on:

- Streamlit Cloud


---

# 🔄 Workflow

```text
User Topic
   ↓
Search Agent
   ↓
Reader Agent
   ↓
Writer Agent
   ↓
Critic Agent
   ↓
Final Research Report
```

---

# 🧪 Example Topics

- AI Agents
- Quantum Computing
- Cybersecurity
- Space Technology
- Future of Robotics

---

# 📦 requirements.txt

```txt
streamlit
langchain
langchain-core
langchain-groq
python-dotenv
requests
beautifulsoup4
tavily-python
rich
```

---

# 👨‍💻 Author

Surendra Yenika
