import os
from agno.agent import Agent
from agno.models.groq import Groq
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.pgvector import PgVector  # This is the correct import path

from utils.embeddings import EmbeddingModel

class DocumentQA:
    """Agent for document question-answering using RAG"""
    
    def __init__(self, db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"):
        # Initialize embedder
        self.embedder = EmbeddingModel()
        # Initialize Groq model
        self.chat_model = Groq(id="llama3-8b-8192")
        # Database URL
        self.db_url = db_url
        self.current_knowledge_base = None
        self.agent = None
        
        print("✅ RAG Agent initialized")
    
    def load_pdf_url(self, url: str, table_name: str = "documents"):
        """Load a PDF from a URL"""
        try:
            # Create PDF URL knowledge base
            self.current_knowledge_base = PDFUrlKnowledgeBase(
                urls=[url],
                vector_db=PgVector(
                    table_name=table_name,
                    db_url=self.db_url,
                    embedder=self.embedder
                ),
            )

            # Initialize the Agent
            self.agent = Agent(
                knowledge=self.current_knowledge_base,
                search_knowledge=True,
                model=self.chat_model
            )

            # Load knowledge base
            print("Loading knowledge base...")
            self.current_knowledge_base.load(recreate=True)
            print("✅ Knowledge base loaded successfully!")

            # Show sample content
            self.show_sample_content()

        except Exception as e:
            print(f"❌ Error loading PDF: {e}")
            import traceback
            print(traceback.format_exc())
    
    def show_sample_content(self, num_samples: int = 5):
        """Show sample content from the knowledge base"""
        try:
            if not self.current_knowledge_base:
                print("No knowledge base loaded!")
                return

            docs = self.current_knowledge_base.search("")
            print("\nSample documents in knowledge base:")
            print("-" * 50)
            for i, doc in enumerate(docs[:num_samples], 1):
                print(f"\nDocument {i}:")
                if hasattr(doc, 'content'):
                    print(doc.content[:200] + "..." if len(doc.content) > 200 else doc.content)
                elif hasattr(doc, 'text'):
                    print(doc.text[:200] + "..." if len(doc.text) > 200 else doc.text)
        except Exception as e:
            print(f"Error showing samples: {e}")
    
    def ask(self, question: str):
        """Ask a question about the loaded document"""
        if not self.current_knowledge_base or not self.agent:
            print("Please load a document first!")
            return

        print(f"\nQ: {question}")
        try:
            # Get relevant documents
            relevant_docs = self.current_knowledge_base.search(question)
            print("\nRelevant documents found:", len(relevant_docs) if relevant_docs else 0)

            # Build context from relevant documents
            context = "\n".join([doc.content if hasattr(doc, 'content') else doc.text
                              for doc in relevant_docs])

            # Create a prompt that includes the context
            full_prompt = f"""Based on the following content:
            
            {context}
            
            Question: {question}
            
            Please provide a detailed answer based ONLY on the information provided above."""

            # Get response with context
            response = self.agent.run(full_prompt)
            return response.content

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            print(traceback.format_exc())
            return f"Error processing question: {str(e)}"