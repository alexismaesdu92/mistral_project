from typing import List, Dict, Any, Optional, Union
import re


SYSTEM_PROMPT = """
You are a helpful AI assistant specialized in answering questions about Mistral AI. Your responses should be:
1. Accurate and based on your knowledge about Mistral AI's models, API, and capabilities
2. Concise and directly addressing the user's query
3. Structured with clear explanations and examples when appropriate
4. Professional but conversational in tone

When answering:
- Focus on providing factual information about Mistral AI's technology, models, and API usage
- If you're unsure about something, acknowledge the limitations of your knowledge
- Prioritize clarity and precision in your explanations
"""
RAG_TASK = """
If the question is unclear or not self-sufficient, refer to the conversation history to clarify the question.
Use the knowledge base to enhance your answer if there is relevant information in it.
When citing information from the knowledge base, ensure your response is coherent and well-integrated.
If the knowledge base contains code examples, adapt them to the user's specific question when appropriate.
"""

NON_RAG_TASK = """
If the question is unclear or not self-sufficient, refer to the conversation history to clarify the question.
Answer based on your general knowledge about Mistral AI, its models, API usage patterns, and best practices.
When you don't have specific information about a topic:
1. Clearly state the limitations of your knowledge
2. Provide general guidance based on similar AI technologies or common practices
3. Suggest what information the user might need to find a more specific answer

Focus on being helpful with what you know rather than speculating about details you're uncertain about.
"""


USER_TEMPLATE = """
{history}
Knowledge base:
{knowledge_base}
User: {query}

Task: {task}
"""




class MessageBuilder:
    def __init__(self, 
                 system_prompt: Optional[str] = None, 
                 user_template:Optional[str] = None,
                 enable_rag: bool = False):
        self.system_prompt = system_prompt or SYSTEM_PROMPT
        self.user_template = user_template or USER_TEMPLATE
        self.enable_rag = enable_rag


    def build_knowledge_base(self, retriving_results):
        if self.enable_rag:
            knowledge_base = ""
            separation ='\n' + '-'*50 + '\n'
            knowledge_base = separation.join([result['text'] for result in retriving_results['result']])
            return knowledge_base
        return "No knowledge base provided"
        

    @staticmethod   
    def convert_chat_message_to_history(chat_message: Dict[str, Any]) -> str:
        role = chat_message.role
        content = chat_message.content
        if role == "user":
            return f"User: {content}"
        elif role == "assistant":
            return f"Assistant: {content}"
        else:
            return ""
    
    def set_rag(self, enable_rag: bool):
        self.enable_rag = enable_rag
        
    def build_history(self, chat_messages: List[Dict[str, Any]]) -> str:
        history = ""
        separation ='\n' + '-'*50 + '\n'
        for chat_message in chat_messages:
            history += self.convert_chat_message_to_history(chat_message) + separation
        return history
    
    def build_system_message(self) -> Dict:
        return {"role": "system", "content": self.system_prompt}
    
    def build_user_message(self, query: str, retrieving_results: Dict[str, Any], history) -> Dict:
        knowledge_base = self.build_knowledge_base(retrieving_results)
        history = self.build_history(history)
        task = RAG_TASK if self.enable_rag else NON_RAG_TASK
        user_message = self.user_template.format(history=history, knowledge_base=knowledge_base, query=query, task=task)
        return {"role": "user", "content": user_message}
        


        

        
