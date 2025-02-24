from knowledge_base import TextFileKnowledgeBase
# Hypothetical imports from Agno framework
from agno.agent import Agent
from agno.models.openai import OpenAIChat

class MediatrenzSupportAgent(Agent):
    def __init__(self):
        # Initialize the knowledge base
        knowledge_base = TextFileKnowledgeBase(file_path='faqs.txt')
        
        # Configure the agent
        super().__init__(
            model=OpenAIChat(id='gpt-4o'),
            description="You are a friendly and helpful customer support agent for Mediatrenz, a digital marketing company.",
            knowledge=knowledge_base,
            memory=True,  # Enable memory for conversation context
            markdown=True  # Support markdown in responses
        )
        self.escalation_keywords = {'urgent', 'problem', 'issue', 'emergency', 'critical'}
        self.escalation_message = (
            "I'm sorry, I can't assist with that directly. You can contact our human support team "
            "via email at **john@mediatrenz.com** or by phone at **1-302-918-5473**."
        )

    def respond(self, query, conversation_id=None):
        """Generate a response to the user's query."""
        query_lower = query.lower()

        # Check for escalation keywords
        if any(keyword in query_lower for keyword in self.escalation_keywords):
            return self.escalation_message

        # Search the knowledge base
        kb_answer = self.knowledge.search(query)
        if kb_answer:
            return kb_answer

        # Fallback response if no match is found
        return self.escalation_message

# Create a singleton instance of the agent
agent = MediatrenzSupportAgent()
