# Financial AI Agents

A comprehensive suite of AI-powered agents for financial analysis, research, and document interaction. This Streamlit application provides an intuitive interface to interact with specialized AI agents for various financial tasks.

## 🚀 Features

- **Stock Analysis Agent**: Get detailed market insights, financial metrics, and trend analysis for any stock ticker
- **Research Agent**: Conduct comprehensive financial research on any topic with web search capabilities
- **Document QA (RAG)**: Ask questions about financial documents using Retrieval Augmented Generation
- **Evaluation Agent**: Assess the quality of RAG system outputs with detailed metrics
- **Reference Tracking**: View and track the sources used by agents during their analyses

## 📋 Requirements

- Python 3.9+
- PostgreSQL with pgvector extension
- API keys for Groq and Phi (Agno)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/kunalsahjwani/financial_ai_agents.git
cd financial_ai_agents
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with:
```
GROQ_API_KEY=your_groq_api_key
PHI_API_KEY=your_phi_api_key
```

5. Set up PostgreSQL with pgvector:
   - Install PostgreSQL
   - Install the pgvector extension
   - Create a database named 'ai' with user 'ai' and password 'ai'
   - The database should be accessible at `localhost:5532`

## 🚀 Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

### Using the App

1. Initialize the agents using the sidebar buttons
2. Navigate to the desired agent tab:
   - **Stock Analysis**: Get financial insights on stocks
   - **Research**: Conduct financial research with web search
   - **Document QA**: Ask questions about financial PDFs
   - **Evaluation**: Assess RAG system outputs
   - **Chat History**: View past interactions
   - **References**: Track sources used by agents

### Stock Analysis Agent

Enter a stock symbol or a comparison query to get detailed market analysis, including:
- Current market position
- Financial metrics
- Competitive analysis
- Forward-looking insights

### Research Agent

Enter any financial research topic to get comprehensive analysis, including:
- Latest trends and developments
- Expert insights and quotes
- Statistical evidence
- Industry impacts and future outlook

### Document QA (RAG)

1. Enter a PDF URL to analyze
2. Ask questions about the document content
3. Get concise, accurate answers based on the document

### Evaluation Agent

Input queries, responses, and context to evaluate RAG system performance across metrics like:
- Faithfulness
- Context relevance
- Answer completeness
- Source attribution
- Response coherence

## 📚 Project Structure

```
financial_ai_agents/
├── agents/
│   ├── __init__.py
│   ├── eval_agent.py       # RAG Evaluation Agent
│   ├── rag_agent.py        # Document QA Agent
│   ├── research_agent.py   # Financial Research Agent
│   └── stock_agent.py      # Stock Analysis Agent
├── utils/
│   ├── __init__.py
│   ├── db_utils.py         # Database utilities
│   └── embeddings.py       # Embedding model wrapper
├── app.py                  # Streamlit application
├── main.py                 # Command-line interface
├── requirements.txt        # Project dependencies
└── .env                    # Environment variables (not tracked by Git)
```

## 🔍 Agent Details

### Stock Analysis Agent
Utilizes Groq's Llama 3 70B model with YFinance tools to provide comprehensive stock market analysis. The agent can:
- Get real-time stock prices
- Analyze financial fundamentals
- Retrieve analyst recommendations
- Access historical price data
- Pull company information and news

### Research Agent
Leverages Groq's Llama 3 70B model with DuckDuckGo and Newspaper4k tools to conduct deep investigative financial research. The agent follows a structured approach:
1. Research Phase: Finding authoritative sources
2. Analysis Phase: Cross-referencing and pattern identification
3. Writing Phase: Creating structured financial reports
4. Quality Control: Fact verification and context addition

### Document QA Agent
Utilizes Groq's Llama 3 8B model with RAG capabilities to answer questions about financial documents. The agent:
- Loads and processes PDF documents
- Creates vector embeddings for efficient retrieval
- Provides contextually relevant answers to specific questions
- Handles complex financial document analysis

### Evaluation Agent
Uses Groq's Llama 3.1 8B model to evaluate RAG system outputs across several key metrics:
- Faithfulness (factual accuracy)
- Context relevance
- Answer completeness
- Source attribution
- Response coherence

## 🔐 Security & Privacy

- API keys are stored in a local `.env` file and not tracked by Git
- No user data is stored or transmitted outside the application
- All analysis happens within the application's runtime environment

## 📜 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- Based on the Agno framework for agent orchestration
- Uses Groq for LLM inference
- Utilizes PgVector for embeddings storage
- Inspired by DataCamp's Financial AI Agents workshop
