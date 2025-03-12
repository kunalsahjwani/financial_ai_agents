import streamlit as st
import os
from dotenv import load_dotenv
import traceback
import re
import datetime
import warnings

# Suppress unnecessary warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Import your existing agents - no changes to these imports
from agents.research_agent import ResearchAgent
from agents.rag_agent import DocumentQA
from agents.stock_agent import StockAnalysisAgent
from agents.eval_agent import RAGEvaluator

# Load environment variables
def load_environment():
    """Load environment variables"""
    load_dotenv()
    
    # Check if required API keys are set
    groq_api_key = os.getenv("GROQ_API_KEY")
    phi_api_key = os.getenv("PHI_API_KEY")
    
    if not groq_api_key:
        st.error("❌ GROQ_API_KEY is not set in .env file")
        return False
    
    if not phi_api_key:
        st.error("❌ PHI_API_KEY is not set in .env file")
        return False
    
    return True

# Initialize session state
def init_session_state():
    if 'research_agent' not in st.session_state:
        st.session_state.research_agent = None
    if 'rag_agent' not in st.session_state:
        st.session_state.rag_agent = None
    if 'stock_agent' not in st.session_state:
        st.session_state.stock_agent = None
    if 'eval_agent' not in st.session_state:
        st.session_state.eval_agent = None
    if 'pdf_loaded' not in st.session_state:
        st.session_state.pdf_loaded = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    # Add this new entry for tracking references
    if 'references' not in st.session_state:
        st.session_state.references = []

# Application header
def show_header():
    st.title("Financial AI Agents")
    st.markdown("""
    A suite of AI-powered agents for financial analysis:
    - 📊 **Stock Analysis** - Get detailed market insights
    - 📝 **Research** - Comprehensive financial research
    - 📄 **Document QA** - Ask questions about financial documents
    - 🔍 **Evaluation** - Assess RAG responses
    - 🔗 **References** - View source links used by agents
    """)

def extract_references(response):
    """Extract URLs from text and return them as a list"""
    urls = []
    
    # Check if it's an agent response object with content attribute
    if hasattr(response, 'content'):
        content = response.content
    else:
        content = str(response)
    
    # Extract URLs with regex from the content
    content_urls = re.findall(r'https?://[^\s\)\]\"\']+', content)
    urls.extend(content_urls)
    
    # Check for tool calls if this is a response from the stock agent or research agent
    if hasattr(response, 'tool_calls') and response.tool_calls:
        for tool_call in response.tool_calls:
            # Extract from tool call arguments
            if hasattr(tool_call, 'arguments') and isinstance(tool_call.arguments, dict):
                for arg_value in tool_call.arguments.values():
                    if isinstance(arg_value, str) and 'http' in arg_value:
                        arg_urls = re.findall(r'https?://[^\s\)\]\"\']+', arg_value)
                        urls.extend(arg_urls)
            
            # Extract from tool call results
            if hasattr(tool_call, 'result'):
                result = tool_call.result
                if isinstance(result, dict):
                    # Handle nested dictionaries or lists in results
                    result_str = str(result)
                    result_urls = re.findall(r'https?://[^\s\)\]\"\']+', result_str)
                    urls.extend(result_urls)
                    
                    # Special case for news articles
                    if 'news' in result:
                        news_items = result.get('news', [])
                        for item in news_items:
                            if isinstance(item, dict) and 'url' in item:
                                urls.append(item['url'])
    
    # Add some default finance references if none found for stock queries
    if not urls and "stock" in str(response).lower():
        # Add some common financial reference URLs
        common_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA"]
        for ticker in common_tickers:
            if ticker.lower() in str(response).lower():
                urls.append(f"https://finance.yahoo.com/quote/{ticker}")
        
        # Extract potential stock symbols from the response
        stock_symbols = re.findall(r'\b[A-Z]{1,5}\b', str(response))
        for symbol in stock_symbols:
            if len(symbol) <= 5 and symbol not in ["A", "I", "THE", "AND", "FOR", "TO"]:
                urls.append(f"https://finance.yahoo.com/quote/{symbol}")
    
    # Remove duplicates while preserving order
    unique_urls = []
    seen = set()
    for url in urls:
        if url not in seen and "http" in url:
            seen.add(url)
            unique_urls.append(url)
    
    return unique_urls

# Initialize agents
def initialize_agents():
    with st.sidebar:
        st.header("Agent Initialization")
        
        # Initialize Stock Analysis Agent
        if st.button("Initialize Stock Agent"):
            with st.spinner("Initializing Stock Analysis Agent..."):
                try:
                    st.session_state.stock_agent = StockAnalysisAgent()
                    st.success("✅ Stock Analysis Agent initialized")
                except Exception as e:
                    st.error(f"Error initializing Stock Analysis Agent: {str(e)}")
        
        # Initialize Research Agent
        if st.button("Initialize Research Agent"):
            with st.spinner("Initializing Research Agent..."):
                try:
                    st.session_state.research_agent = ResearchAgent()
                    st.success("✅ Research Agent initialized")
                except Exception as e:
                    st.error(f"Error initializing Research Agent: {str(e)}")
        
        # Initialize RAG Agent
        if st.button("Initialize RAG Agent"):
            with st.spinner("Initializing RAG Agent..."):
                try:
                    st.session_state.rag_agent = DocumentQA()
                    st.success("✅ RAG Agent initialized")
                except Exception as e:
                    st.error(f"Error initializing RAG Agent: {str(e)}")
        
        # Initialize Evaluation Agent
        if st.button("Initialize Evaluation Agent"):
            with st.spinner("Initializing Evaluation Agent..."):
                try:
                    st.session_state.eval_agent = RAGEvaluator()
                    st.success("✅ Evaluation Agent initialized")
                except Exception as e:
                    st.error(f"Error initializing Evaluation Agent: {str(e)}")

# Stock analysis tab
def stock_analysis_tab():
    st.header("Stock Analysis")
    
    if st.session_state.stock_agent is None:
        st.warning("Please initialize the Stock Analysis Agent from the sidebar first.")
        return
    
    query = st.text_area("Enter a stock query (e.g., 'AAPL' or 'Compare MSFT and GOOGL')", height=100)
    
    if st.button("Analyze Stock") and query:
        with st.spinner("Analyzing stock data..."):
            try:
                response = st.session_state.stock_agent.analyze(query)
                
                # Extract references with improved function
                urls = extract_references(response)
                
                # If no URLs found, try to extract stock symbols
                if not urls:
                    # Extract potential stock symbols from the query and response
                    stock_symbols = set(re.findall(r'\b[A-Z]{1,5}\b', query.upper() + " " + str(response)))
                    # Filter common words that might be captured as symbols
                    common_words = {"A", "I", "THE", "AND", "FOR", "TO", "IN", "OF", "ON"}
                    stock_symbols = [s for s in stock_symbols if s not in common_words and len(s) <= 5]
                    
                    for symbol in stock_symbols:
                        urls.append(f"https://finance.yahoo.com/quote/{symbol}")
                
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                for url in urls:
                    st.session_state.references.append((query, "Stock Analysis", url, timestamp))
                
                st.session_state.chat_history.append(("Stock Query", query))
                st.session_state.chat_history.append(("Stock Analysis", response))
                st.markdown(response)
                
                # Show reference count
                if urls:
                    st.success(f"Found {len(urls)} references. View them in the References tab.")
            except Exception as e:
                st.error(f"Error analyzing stock: {str(e)}")
                st.code(traceback.format_exc())

# Research tab
def research_tab():
    st.header("Financial Research")
    
    if st.session_state.research_agent is None:
        st.warning("Please initialize the Research Agent from the sidebar first.")
        return
    
    query = st.text_area("Enter a research topic", height=100)
    
    if st.button("Research") and query:
        with st.spinner("Conducting research..."):
            try:
                response = st.session_state.research_agent.run(query)
                
                # Extract references
                urls = extract_references(response)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                for url in urls:
                    st.session_state.references.append((query, "Research", url, timestamp))
                
                st.session_state.chat_history.append(("Research Query", query))
                st.session_state.chat_history.append(("Research Results", response))
                st.markdown(response)
                
                # Show reference count
                if urls:
                    st.success(f"Found {len(urls)} references. View them in the References tab.")
            except Exception as e:
                st.error(f"Error conducting research: {str(e)}")

# Document QA tab
def document_qa_tab():
    st.header("Document Question Answering")
    
    if st.session_state.rag_agent is None:
        st.warning("Please initialize the RAG Agent from the sidebar first.")
        return
    
    # PDF URL input
    pdf_url = st.text_input("Enter a PDF URL to analyze")
    
    if st.button("Load PDF") and pdf_url:
        with st.spinner("Loading PDF..."):
            try:
                st.session_state.rag_agent.load_pdf_url(pdf_url)
                st.session_state.pdf_loaded = True
                st.success("PDF loaded successfully!")
                
                # Add the PDF URL as a reference
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.references.append(("PDF Document", "Document Load", pdf_url, timestamp))
            except Exception as e:
                st.error(f"Failed to load PDF: {str(e)}")
    
    # Question input
    if st.session_state.pdf_loaded:
        question = st.text_input("Ask a question about the document")
        
        if st.button("Ask") and question:
            with st.spinner("Finding answer..."):
                try:
                    # Direct call to your existing ask method
                    response = st.session_state.rag_agent.ask(question)
                    st.session_state.chat_history.append(("Document Question", question))
                    st.session_state.chat_history.append(("Document Answer", response))
                    st.markdown(response)
                except Exception as e:
                    st.error(f"Error processing question: {str(e)}")
                    # Message to user on what to try instead
                    st.info("If you're encountering errors with the RAG agent, try:")
                    st.info("1. Using a simpler question")
                    st.info("2. Using a different PDF document")
                    st.info("3. Checking the console logs for detailed error information")
    else:
        st.info("Please load a PDF document first.")

# Evaluation tab
def evaluation_tab():
    st.header("RAG Evaluation")
    
    if st.session_state.eval_agent is None:
        st.warning("Please initialize the Evaluation Agent from the sidebar first.")
        return
    
    query = st.text_input("Query")
    response = st.text_area("Response to evaluate", height=150)
    context = st.text_area("Context (separate multiple contexts with commas)", height=150)
    
    if st.button("Evaluate") and query and response:
        with st.spinner("Evaluating response..."):
            try:
                context_list = [c.strip() for c in context.split(",")]
                evaluation = st.session_state.eval_agent.evaluate(query, response, context_list)
                st.session_state.chat_history.append(("Evaluation Request", f"Query: {query}"))
                st.session_state.chat_history.append(("Evaluation Results", evaluation))
                st.markdown(evaluation)
            except Exception as e:
                st.error(f"Error during evaluation: {str(e)}")

# Chat history tab
def chat_history_tab():
    st.header("Chat History")
    
    if not st.session_state.chat_history:
        st.info("No chat history yet.")
        return
    
    for i, (sender, message) in enumerate(st.session_state.chat_history):
        if i % 2 == 0:  # User message
            st.info(f"**{sender}**: {message}")
        else:  # Agent response
            with st.expander(f"{sender} (Click to expand/collapse)"):
                st.markdown(message)
    
    if st.button("Clear History"):
        st.session_state.chat_history = []
        st.experimental_rerun()

# References tab
def references_tab():
    st.header("Reference Links")
    
    if not st.session_state.references:
        st.info("No references tracked yet. Run queries with the Research or Stock Analysis agents to generate references.")
        return
    
    # Group references by query
    queries = {}
    for ref_info in st.session_state.references:
        if len(ref_info) == 4:  # Ensure proper format
            query, ref_type, ref_link, timestamp = ref_info
            if query not in queries:
                queries[query] = []
            queries[query].append((ref_type, ref_link, timestamp))
    
    # Display references grouped by query
    for query, refs in queries.items():
        with st.expander(f"Query: {query}", expanded=True):
            for i, (ref_type, ref_link, timestamp) in enumerate(refs, 1):
                st.markdown(f"**Reference {i}** ({ref_type}) - {timestamp}")
                st.markdown(f"[{ref_link}]({ref_link})")
            
    if st.button("Clear References"):
        st.session_state.references = []
        st.experimental_rerun()

# Function to add custom CSS
def apply_custom_css():
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .reportview-container .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Main app
def main():
    # Apply custom CSS
    apply_custom_css()
    
    # Load environment variables
    if not load_environment():
        st.error("Failed to load environment variables. Please check your .env file.")
        return
    
    # Initialize session state
    init_session_state()
    
    # Display header
    show_header()
    
    # Initialize agents sidebar
    initialize_agents()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Stock Analysis", 
        "Research", 
        "Document QA", 
        "Evaluation",
        "Chat History",
        "References"  # New tab
    ])
    
    # Populate tabs
    with tab1:
        stock_analysis_tab()
    
    with tab2:
        research_tab()
    
    with tab3:
        document_qa_tab()
    
    with tab4:
        evaluation_tab()
    
    with tab5:
        chat_history_tab()
        
    with tab6:
        references_tab()  # New tab function

if __name__ == "__main__":
    # Run the app
    main()