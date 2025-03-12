from textwrap import dedent
from agno.agent import Agent
from agno.models.groq import Groq

class RAGEvaluator:
    """Agent for evaluating RAG system outputs"""
    
    def __init__(self):
        self.evaluator = Agent(
            model=Groq(id="llama-3.1-8b-instant"),
            description=dedent("""\
                You are an expert RAG system evaluator with deep expertise in:
                - Information retrieval quality assessment
                - Response accuracy evaluation
                - Source attribution verification
                - Context relevance analysis
                - Natural language generation evaluation
            """),
            instructions=dedent("""\
                Evaluate the RAG system output based on these key metrics:

                1. Faithfulness (1-5):
                   - How accurately does the response reflect the source documents?
                   - Are there any hallucinations or incorrect statements?
                   - Does it maintain factual consistency?

                2. Context Relevance (1-5):
                   - Are the retrieved passages relevant to the query?
                   - Is important context missing?
                   - Is irrelevant information included?

                3. Answer Completeness (1-5):
                   - Does the response fully address the query?
                   - Are all key aspects covered?
                   - Is the level of detail appropriate?

                4. Source Attribution (1-5):
                   - Are sources properly cited?
                   - Is it clear which information comes from where?
                   - Can claims be traced back to sources?

                5. Response Coherence (1-5):
                   - Is the response well-structured?
                   - Does it flow logically?
                   - Is it easy to understand?

                Provide specific examples and explanations for each score.
            """),
            expected_output=dedent("""\
                # RAG Evaluation Report

                ## Overview
                Query: {query}
                Response Length: {n_chars} characters

                ## Metric Scores

                ### Faithfulness: {score}/5
                - Justification:
                - Examples:
                - Areas for Improvement:

                ### Context Relevance: {score}/5
                - Justification:
                - Examples:
                - Areas for Improvement:

                ### Answer Completeness: {score}/5
                - Justification:
                - Examples:
                - Areas for Improvement:

                ### Source Attribution: {score}/5
                - Justification:
                - Examples:
                - Areas for Improvement:

                ### Response Coherence: {score}/5
                - Justification:
                - Examples:
                - Areas for Improvement:

                ## Overall Score: {total}/25

                ## Key Recommendations
                1. {rec1}
                2. {rec2}
                3. {rec3}

                ## Summary
                {final_assessment}
            """),
            markdown=True,
        )
        
        print("✅ RAG Evaluator initialized")
    
    def evaluate(self, query, response, context):
        """
        Evaluate a RAG system's response
        
        Args:
            query (str): Original user query
            response (str): RAG system's response
            context (list): Retrieved passages used for the response
        """
        evaluation_prompt = f"""
        Please evaluate this RAG system output:

        QUERY:
        {query}

        RETRIEVED CONTEXT:
        {' '.join(context)}

        RESPONSE:
        {response}

        Provide a detailed evaluation following the metrics and format specified.
        """

        try:
            evaluation = self.evaluator.run(evaluation_prompt)
            return evaluation.content
        except Exception as e:
            print(f"Error evaluating response: {e}")
            return f"Error: {str(e)}"