from textwrap import dedent
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools

class StockAnalysisAgent:
    """Agent for stock market analysis"""
    
    def __init__(self):
        self.agent = Agent(
            model=Groq(id="llama3-70b-8192"),
            tools=[
                YFinanceTools(
                    stock_price=True,
                    analyst_recommendations=True,
                    stock_fundamentals=True,
                    historical_prices=True,
                    company_info=True,
                    company_news=True,
                )
            ],
            instructions=dedent("""\
                You are a seasoned credit rating analyst with deep expertise in market analysis! 📊

                Follow these steps for comprehensive financial analysis:
                1. Market Overview
                   - Latest stock price
                   - 52-week high and low
                2. Financial Deep Dive
                   - Key metrics (P/E, Market Cap, EPS)
                3. Market Context
                   - Industry trends and positioning
                   - Competitive analysis
                   - Market sentiment indicators

                Your reporting style:
                - Begin with an executive summary
                - Use tables for data presentation
                - Include clear section headers
                - Highlight key insights with bullet points
                - Compare metrics to industry averages
                - Include technical term explanations
                - End with a forward-looking analysis

                Risk Disclosure:
                - Always highlight potential risk factors
                - Note market uncertainties
                - Mention relevant regulatory concerns
                
            """),
            add_datetime_to_instructions=True,
            show_tool_calls=True,
            markdown=True,
        )
        
        print("✅ Stock Analysis Agent initialized")
    
    def analyze(self, query):
        """Analyze stocks based on query"""
        try:
            response = self.agent.run(query)
            return response.content
        except Exception as e:
            print(f"Error analyzing stocks: {e}")
            return f"Error: {str(e)}"