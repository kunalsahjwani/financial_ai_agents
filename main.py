import os
from dotenv import load_dotenv
from agents.research_agent import ResearchAgent
from agents.rag_agent import DocumentQA
from agents.stock_agent import StockAnalysisAgent
from agents.eval_agent import RAGEvaluator

def load_environment():
    """Load environment variables"""
    load_dotenv()
    
    # Check if required API keys are set
    groq_api_key = os.getenv("GROQ_API_KEY")
    phi_api_key = os.getenv("PHI_API_KEY")
    
    if not groq_api_key:
        print("❌ GROQ_API_KEY is not set in .env file")
        return False
    
    if not phi_api_key:
        print("❌ PHI_API_KEY is not set in .env file")
        return False
    
    print("✅ Environment variables loaded successfully")
    return True

def demo_rag_agent():
    """Demonstrate RAG agent capabilities"""
    print("\n=== RAG Agent Demo ===")
    rag_qa = DocumentQA()
    rag_qa.load_pdf_url("https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2024.pdf")
    
    # Ask questions
    questions = [
        "What are the key points in this report? Give in 5 bullets",
        "Executive Summary in 100 words"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        answer = rag_qa.ask(question)
        print(f"Answer: {answer}")

def demo_research_agent():
    """Demonstrate research agent capabilities"""
    print("\n=== Research Agent Demo ===")
    research_agent = ResearchAgent()
    
    query = "Analyze the current state and future implications of artificial intelligence in Finance"
    print(f"\nQuery: {query}")
    response = research_agent.run(query)
    print(f"Response: {response[:500]}...[truncated]")

def demo_stock_agent():
    """Demonstrate stock analysis agent capabilities"""
    print("\n=== Stock Analysis Agent Demo ===")
    stock_agent = StockAnalysisAgent()
    
    query = "What's the latest news and financial performance of Apple (AAPL)?"
    print(f"\nQuery: {query}")
    response = stock_agent.analyze(query)
    print(f"Response: {response[:500]}...[truncated]")

def demo_eval_agent():
    """Demonstrate evaluation agent capabilities"""
    print("\n=== Evaluation Agent Demo ===")
    evaluator = RAGEvaluator()
    
    query = "What are the key features of transformer models?"
    context = [
        "Transformer models use self-attention mechanisms to process input sequences.",
        "Key features include parallel processing and handling of long-range dependencies."
    ]
    response = "Transformer models are characterized by their self-attention mechanism..."
    
    print(f"\nEvaluating a sample RAG response:")
    evaluation = evaluator.evaluate(query, response, context)
    print(f"Evaluation: {evaluation[:500]}...[truncated]")

def main():
    """Main entry point"""
    if not load_environment():
        return
    
    print("Financial AI Agents Demo")
    print("=" * 50)
    
    # Uncomment the demos you want to run:
    demo_rag_agent()
    demo_research_agent()
    demo_stock_agent()
    demo_eval_agent()
    
    print("\nTo run a specific demo, uncomment the corresponding function in main.py")

# Add this at the bottom of your main.py file

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python main.py [rag|research|stock|evaluate] [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "rag":
        if len(sys.argv) < 4:
            print("Usage: python main.py rag [pdf_url] [question]")
            sys.exit(1)
        
        pdf_url = sys.argv[2]
        question = sys.argv[3]
        
        rag_qa = DocumentQA()
        rag_qa.load_pdf_url(pdf_url)
        answer = rag_qa.ask(question)
        print(answer)
    
    elif command == "research":
        if len(sys.argv) < 3:
            print("Usage: python main.py research [topic]")
            sys.exit(1)
        
        topic = sys.argv[2]
        research_agent = ResearchAgent()
        result = research_agent.run(topic)
        print(result)
    
    elif command == "stock":
        if len(sys.argv) < 3:
            print("Usage: python main.py stock [query]")
            sys.exit(1)
        
        query = sys.argv[2]
        stock_agent = StockAnalysisAgent()
        result = stock_agent.analyze(query)
        print(result)
    
    elif command == "evaluate":
        if len(sys.argv) < 5:
            print("Usage: python main.py evaluate [query] [response] [context_csv]")
            sys.exit(1)
        
        query = sys.argv[2]
        response = sys.argv[3]
        context_csv = sys.argv[4]
        context_list = context_csv.split(",")
        
        evaluator = RAGEvaluator()
        result = evaluator.evaluate(query, response, context_list)
        print(result)
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: rag, research, stock, evaluate")
        sys.exit(1)